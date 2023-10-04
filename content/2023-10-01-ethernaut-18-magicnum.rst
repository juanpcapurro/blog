###########################
Ethernaut 18: MagicNum
###########################
:date: 2023-10-01
:slug: ethernaut-18-magicnum
:summary: I had to use inline assembly to deploy my hand-crafted assembly
:tags: programming
:author: capu
:featured_image:

Objective
=========
Create a ``solver`` contract, which:

- has a codesize of 10 or lower.
- returns the number 42 when the ``whatIsTheMeaningOfLife()`` method is invoked
  on it.

`The level description <https://ethernaut.openzeppelin.com/level/18>`_ is clear
about it: it's time to hand-write some EVM bytecode. Even an empty Solidity
contract would be too big, the logic of rejecting eth transfers or unknown
method calls would be bloat if I want to stay under 10 bytes.

Code
====
.. code-block:: solidity
    :linenos: inline

    pragma solidity ^0.8.13;

    contract MagicNum {
        address public solver;

        constructor() {}

        function setSolver(address _solver) public {
            solver = _solver;
        }

        /*
        ____________/\\\_______/\\\\\\\\\_____        
        __________/\\\\\_____/\\\///////\\\___       
        ________/\\\/\\\____\///______\//\\\__      
        ______/\\\/\/\\\______________/\\\/___     
        ____/\\\/__\/\\\___________/\\\//_____    
        __/\\\\\\\\\\\\\\\\_____/\\\//________   
        _\///////////\\\//____/\\\/___________  
        ___________\/\\\_____/\\\\\\\\\\\\\\\_ 
        ___________\///_____\///////////////__
        */
    }


Solution
========

I love this challenge. It's incrediby simple, yet an excuse to
learn a bit of yul plus go through how ``CREATE`` works again!

This problem has three parts:

1. Devise a contract capable of returning the integer '42' when a method
   ``whatIsTheMeaningOfLife()`` is invoked on it. using less than 10 bytes.
2. Figure out what the deployment code for ^ is.
3. Plumb it through my foundry project.

1. The contract
---------------
It should:

- Load the value 42 into memory
- Load the offset and length of the return data onto the stack
- Call return

So something like:

.. code-block:: plain

    00 PUSH1 2A    // [2A]
    02 PUSH1 1F    // [2A 1F]
    04 MSTORE8     // [] -- stored 0x2A/42 in memory position 1F
    05 PUSH1 20    // [20]
    07 PUSH0       // [00 20]
    08 RETURN      // [] -- returned bytes from 00-20 of memory

should work. And it only uses 9 bytes!

.. note ::

    Before the shanghai hardfork this required 10 opcodes, but now it's solvable
    with 9, because the introduction of opcode ``PUSH0``. It allows to push an
    empty word to the stack in a single byte, where before it was necessary to
    do ``PUSH1 00``, which took two.

Also, note that my contract returns 42 to calls on ``whatIsTheMeaningOfLife()``,
but also on ether transfers, calls to ``foobar2000()``, or whatever else. It's
not a requirement to *only* return 42 on calls to the aforementioned method
name, and that's for the better, because I couldn't fit it in 10 bytes anyway.

2. The deployment code
----------------------

as I've gone through in the `second evm puzzles blog post
<{filename}/2023-04-24-evm-puzzles-2.rst>`_, the contract creation code actually
has to 'return' the bytecode that'll constitute the new contract:

.. code-block:: plain

    00 PUSH1 09     // [09]
    02 PUSH1 0A     // [09 0A]
    04 PUSH0        // [09 0A 00]
    05 CODECOPY     // -- copied the desired code to memory
    06 PUSH1 09     // [09]
    08 PUSH0        // [09 00]
    09 RETURN       // [] -- 'return' the copied memory
    0A PUSH1 2A     //  ---
    0C PUSH1 1F     // |
    0E MSTORE8      // | the code from
    0f PUSH1 20     // | before
    11 PUSH0        // |
    12 RETURN       //  ---

some smol manual assemblin' yields the code for this should be:

``0x6009600a5f3960095ff3602a601f5360205ff3``

3. The plumbing
---------------
Simplest thing I think will be to use yul, since it comes bundled with solidity.
This means I had to manually re-assemble the deployment code for every time I
tried a different one. It's okay for a small contract like this one, but it
wouldn't scale well for other things:

.. code-block:: solidity

    bytes19 constant private creationCode =
        0x6009600a5f3960095ff3602a601f5360205ff3;

    function solution(address payable target_) internal override{
        MagicNum target = MagicNum(target_);
        address deployment;
        assembly {
            // from the yul docs
            function allocate(size) -> ptr {
                ptr := mload(0x40)
                if iszero(ptr) { ptr := 0x60 }
                mstore(0x40, add(ptr, size))
            }
            let offset := allocate(19)
            mstore(offset, creationCode)
            deployment := create(0, offset, 19)
        }
        target.setSolver(deployment);
    }

.. note::

    I have to allocate the variable manually to know the memory index of where the
    creation code will be stored. I could put the code on a memory variable, read
    the free memory pointer and subtract the presumed size of the variable to get
    where it is on a 'regular' variable, but I believe that'd be more fragile, since
    the layout in memory of variables is not part of any 'interface' and I would get
    no guarantees about it staying the same with different compiler versions or
    optimizer settings.
