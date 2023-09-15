################################
Let's play some more EVM Puzzles
################################
:date: 2023-04-24
:summary: some day I'll gather the courage to livestream these things
:slug: evm-puzzles-2
:tags: programming
:author: capu
:featured_image:

This post covers `EVM Puzzles <https://github.com/fvictorio/evm-puzzles>`_
6-10. If you want to see the others, you should check out the `first post
<{filename}/2023-04-14-evm-puzzles-1.rst>`_

Puzzle 6
========

.. code-block:: plain

    00      6000      PUSH1 00     // [ 00 ]
    02      35        CALLDATALOAD // [ DATA[0] ] first *word* (32 bytes)
    03      56        JUMP         // [  ] jumped to DATA[0]
    04      FD        REVERT
    05      FD        REVERT
    06      FD        REVERT
    07      FD        REVERT
    08      FD        REVERT
    09      FD        REVERT
    0A      5B        JUMPDEST
    0B      00        STOP

So I just have to send ``0A`` as calldata, and it'll jump to ``0A``. Easy peasy.

.. code-block:: plain

    ? Enter the calldata: 0x0A
    Wrong solution :(

😭 no lemon squeezy. Perhaps it's some endianness thing? let's specify the whole word:

.. note::

    In Vim you can do ``i0x<esc>62a0<esc>a0A<esc>`` to craft the following
    string. I like it because it after this kind of thing is commited to muscle
    memory, I can craft specific strings without engaging any neuron higher
    than my shoulders, leaving my mind free to think of more interesting
    problems, such as un-breaking my linter or achieveing 'syntax' highlighting
    with only lexical analysis

.. code-block:: plain

    ? Enter the calldata: 0x000000000000000000000000000000000000000000000000000000000000000A
    Puzzle solved!

Okay. I solved the puzzle. But just solving it is not enough. I need to
*comprehensively understand* why it is that it works that way. If you're not
sure about this *need*, then `Terence Parr can radicalize you too with his post
about the essentials of debugging
<https://blog.parr.us/2014/11/17/the-essentials-of-debugging/>`_. 

Thankfully it's 2023 and there are nice well-abstracted tools to help with
that. Let's use evm.codes, with the `link provided by the game itself
<https://www.evm.codes/playground?callValue=0&unit=Wei&callData=0x0A&codeType=Bytecode&code=%2760003556FDFDFDFDFDFD5B00%27_&fork=shanghai>`_

.. image:: {static}/evm-puzzles-2/6.png

.. image:: {static}/evm-puzzles-2/6-1.png

If I only provide ``0x0a``, then the left padding is *removed??* and then it's padded to the right?

``echo -n "a00000000000000000000000000000000000000000000000000000000000000"| wc
-c`` is ``63``. So the calldata isn't getting its bytes split in half. Zeroes on
the left are just not displayed in the UI. That would've been extermely weird,
in retrospect. But there's probably something to learn about how the calldata is
encoded and decoded.

Remember that a machine can be little-endian or big-endian. As a refresher,
imagine an ``uint16_t`` in a 32 bit machine with the value "420". Or
``0x1A4``. In memory, it can be stored as both:

.. code-block:: plain

    value:        00 00 01 A4
    memory index: 00 01 02 03

.. code-block:: plain

    value:        A4 01 00 00
    memory index: 00 01 02 03

which one is little-endian? and which is big-endian?

Don't worry, I had to look it up too. 

    A big-endian system stores the most significant byte of a word at the smallest
    memory address and the least significant byte at the largest. A little-endian
    system, in contrast, stores the least-significant byte at the smallest address

The first one is the big-endian.

Coming back to our 32-byte word world: calldata is ``0x0A``. When reading the
CALLDATALOAD instruction, the machine reads 'the smallest :strike:`memory`
calldata address' (index 0, value ``0A``) and puts into the 'most significant
byte' in the stack slot. Then it'd grab another byte, with index 1, but there's no
more calldata. So the instruction finishes executing, and since in Ethereum
anything that you don't deliberately initialize is a zero, you get
``0x0A00000000000000000000000000000000000000000000000000000000000000`` in the
stack.

Puzzle 7
========

.. code-block:: plain

    00      36        CALLDATASIZE // [ len(DATA) ]
    01      6000      PUSH1 00     // [ 00 len(DATA) ]
    03      80        DUP1         // [ 00 00 len(DATA) ]
    04      37        CALLDATACOPY // [  ] -- copies calldata into memory, indices stay the same
                                   // since its form index 0 to index 0
    05      36        CALLDATASIZE // [ len(DATA) ]
    06      6000      PUSH1 00     // [ 00 len(DATA) ]
    08      6000      PUSH1 00     // [ 00 00 len(DATA) ]
    0A      F0        CREATE       // [ NEWADDR ] -- created another contract with entire calldata
                                   // as contract creation code
    0B      3B        EXTCODESIZE  // [ contract_size(NEWADDR) ]
    0C      6001      PUSH1 01     // [ 01 contract_size(NEWADDR) ]
    0E      14        EQ           // [ 01==contract_size(NEWADDR) ]
    0F      6013      PUSH1 13     // [ 13 01==contract_size(NEWADDR) ]
    11      57        JUMPI        // -- jumped to 13 if 01==contract_size(NEWADDR)
    12      FD        REVERT       //
    13      5B        JUMPDEST     //
    14      00        STOP         //

To solve this I should provide a calldata such that a contract is deployed with code size 1.

I have postponed learning how the contract creation code is actually constructed for the longest
time.
So it's abount time I look it up.

To start, let's look at the creation code of an empty contract. Keep in mind that even a contract
which has no solidity code to its name will still have some bytecode in it's implementation, since
it'll, for example, care to REVERT if ether is sent to it, since that's what a Solidity contract
with no fallback/receive function is specified to do.

Let's debug the birth of a contract with Foundry:

.. code-block:: plain

    contract C {}

    contract CreationDemo is Test {
        function test() public {
            console.logBytes(type(C).creationCode);
            address a = address(new C());
            console.logBytes(a.code);
            console.log(a);
        }
    }

.. code-block:: plain

    Running 1 test for test/Counter.t.sol:CreationDemo
    [PASS] test() (gas: 49750)
    Logs:
    0x6080604052348015600f57600080fd5b50603f80601d6000396000f3fe6080604052600080fdfea2646970667358221220f426492e214b341eb0f2a6416e18476a52860939a3ab4fc0f6d0bb61235bd11464736f6c63430008130033
    0x6080604052600080fdfea2646970667358221220f426492e214b341eb0f2a6416e18476a52860939a3ab4fc0f6d0bb61235bd11464736f6c63430008130033
    0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f

    Test result: ok. 1 passed; 0 failed; finished in 525.74µs

knowing these three values, let's run the thing opcode-by-opcode with ``forge test --debug test``

.. code-block:: plain

    ┌Address: 0x7fa9385be102ac3eac297483dd6233d62b3e1496 | PC: 1970 | Gas used in call: 3718─────────────────────────────────────┐
    │07ad| SWAP2                                                                                                                 │
    │07ae| SUB                                                                                                                   │
    │07af| SWAP1                                                                                                                 │
    │07b0| PUSH1(0x00)                                                                                                           │
    │07b2|▶CREATE                                                                                                                │
    │END CALL                                                                                                                    │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ┌Stack: 6────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │00| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | value                 │
    │01| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 c4 | offset                │
    │02| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 5c | size                  │
    │03| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |                       │
    │04| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 3e |                       │
    │05| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f8 a8 fd 6d |                       │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌Memory (max expansion: 544 bytes)───────────────────────────────────────────────────────────────────────────────────────────┐
    │160| 00 00 00 5c 60 80 60 40 52 34 80 15 60 0f 57 60 00 80 fd 5b 50 60 3f 80 60 1d 60 00 39 60 00 f3 |...\..`W`..``..       │
    │180| fe 60 80 60 40 52 60 00 80 fd fe a2 64 69 70 66 73 58 22 12 20 f4 26 49 2e 21 4b 34 1e b0 f2 a6 |.@R`..dipfsX"..!K4.   │
    │1a0| 41 6e 18 47 6a 52 86 09 39 a3 ab 4f c0 f6 d0 bb 61 23 5b d1 14 64 73 6f 6c 63 43 00 08 13 00 33 |AnG....dsolcC..3      │
    │1c0| 00 00 00 00 60 80 60 40 52 34 80 15 60 0f 57 60 00 80 fd 5b 50 60 3f 80 60 1d 60 00 39 60 00 f3 |......`W`..``..       │
    │1e0| fe 60 80 60 40 52 60 00 80 fd fe a2 64 69 70 66 73 58 22 12 20 f4 26 49 2e 21 4b 34 1e b0 f2 a6 |.@R`..dipfsX"..!K4.   │
    │200| 41 6e 18 47 6a 52 86 09 39 a3 ab 4f c0 f6 d0 bb 61 23 5b d1 14 64 73 6f 6c 63 43 00 08 13 00 33 |AnG....dsolcC..3      │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

First, let's look into the parameters for the CREATE opcode:

- value of zero
- start from memory position ``0x1c4``
- use ``0x5c`` bytes from there (up to memory address ``0x220``)

``6080604052348015600f57600080fd5b50603f80601d6000396000f3fe6080604052600080fdfea2646970667358221220f426492e214b341eb0f2a6416e18476a52860939a3ab4fc0f6d0bb61235bd11464736f6c63430008130033``.
Exactly the same as the ``type(C).creationCode``. No surprises here.

I ran the contract initialization step by step to fully understand its execution, but the gist of it
is:

.. code-block:: plain

    00: PUSH1 0x80  //
    02: PUSH1 0x40  // solidity's memory initialization,
    04: MSTORE      // every solidity contract has this

    05: CALLVALUE //
    06: DUP1      // 
    07: ISZERO    //
    08: PUSH1 0xf // this contract doesn't have a payable constructor,
    0a: JUMPI     // so this exists here to revert if a value other
    0b: PUSH1 0x0 // than zero is provided
    0d: DUP1      //
    0e: REVERT    //

    0f: JUMPDEST   //
    10: POP        //
    11: PUSH1 0x3f // copy, to memory address zero, the code from 1d up
    13: DUP1       // to 3f+1d = 5C
    14: PUSH1 0x1d //
    16: PUSH1 0x0  //
    18: CODECOPY   // 

    19: PUSH1 0x0  // return, indicating return data as the code copied
    1b: RETURN     // to memory above

    1c: INVALID    // 0xFE, designated invalid opcode. seems to be padding
                   // so the entire code can be retrieved in two words
                   // instead of three

    1d: PUSH1 0x80 //
    1f: PUSH1 0x40 //
    ...            // the aforementioned code
    5a: STOP       //
    5b: CALLER     //

The contract initialization code seems to return another piece of valid bytecode: ``6080604052600080fdfea2646970667358221220f426492e214b341eb0f2a6416e18476a52860939a3ab4fc0f6d0bb61235bd11464736f6c63430008130033``.
This seems to be the code that's actually deployed.

more so, when continuing the execution, I the CREATE opcode has pushed the address for the new
contract to the stack, and nothing related to the bytecode just 'returned' [1]_ .

.. code-block:: plain

    ┌Address: 0x7fa9385be102ac3eac297483dd6233d62b3e1496 | PC: 1971 | Gas used in call: 48384────────────┐
    │07b3|▶DUP1                                                                                          │
    │07b4| ISZERO                                                                                        │
    │07b5| DUP1                                                                                          │
    │07b6| ISZERO                                                                                        │
    │07b7| PUSH2(0x07c4)                                                                                 │
    │07ba| JUMPI                                                                                         │
    └────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ┌Stack: 4────────────────────────────────────────────────────────────────────────────────────────────┐
    │00| 00 00 00 00 00 00 00 00 00 00 00 00 56 15 de b7 98 bb 3e 4d fa 01 39 df a1 b3 d4 33 cc 23 b7 2f │
    │01| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 │
    │02| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 3e │
    │03| 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f8 a8 fd 6d │
    │                                                                                                    │
    │                                                                                                    │
    └────────────────────────────────────────────────────────────────────────────────────────────────────┘

So, if I understood correctly, contract creation works as follows:

- pass a value (not important here) and  memory range to the CREATE opcode
- the memory range is set as a one-time bytecode for the contract, and starts executing
- this one-time bytecode is expected to return the actual bytecode for the new contract.

let's try it out then. I shoud craft some bytecode returning a one-byte value.

.. code-block:: plain

    00 PUSH1 01 // [01]
    02 PUSH1 00 // [00 01]
    04 RETURN   // [] -- return data from memory addresses 0 to 1

serialized, it should be: ``0x60016000F3``. Although I'm referencing memory that I haven't
initialized, perhaps that'll yield an error?

.. code-block:: plain

    ? Enter the calldata: 0x60016000F3

    Puzzle solved!

😎 

Puzzle 8
========

.. code-block:: plain

    00      36        CALLDATASIZE // [ len(DATA) ]
    01      6000      PUSH1 00     // [ 00 len(DATA) ]
    03      80        DUP1         // [ 00 00 len(DATA) ]
    04      37        CALLDATACOPY // [] -- all of calldata is copied to memory
    05      36        CALLDATASIZE // [ len(DATA) ]
    06      6000      PUSH1 00     // [ 00 len(DATA) ]
    08      6000      PUSH1 00     // [ 00 00 len(DATA) ]
    0A      F0        CREATE       // [  ] -- create contract with value 0 and the
                                   // calldata as initialization bytecode
    0B      6000      PUSH1 00     // [ 00 newaddr ]
    0D      80        DUP1         // [ 00 00 newaddr ]
    0E      80        DUP1         // [ 00 00 00 newaddr ]
    0F      80        DUP1         // [ 00 00 00 newaddr ]
    10      80        DUP1         // [ 00 00 00 00 newaddr ]
    11      94        SWAP5        // [ newaddr 00 00 00 00 ]
    12      5A        GAS          // [ gas_left newaddr 00 00 00 00 ]
    13      F1        CALL         // [ retval ] -- call the recently deployed contract
                                   // with all the gas and no argumentss
    14      6000      PUSH1 00     // [ 00 retval ]
    16      14        EQ           // [ 00==retval ]
    17      601B      PUSH1 1B     // [ 1B 00==retval ]
    19      57        JUMPI        // [  ] -- jumped to 1B if 00==retval
    1A      FD        REVERT       //
    1B      5B        JUMPDEST     //
    1C      00        STOP         //

this is mostly like the previous one, but instead of there being restrictions on the size of the
contract, it should revert. Will a single revert opcode work?

.. code-block:: plain

    00 PUSH1 FD // [ FD ]
    02 PUSH2 00 // [ 00 FD ]
    04 MSTORE8  // [ ] -- FD in position 00 in memory
    05 PUSH1 01 // [01]
    07 PUSH1 00 // [00 01]
    09 RETURN   // [] -- return data from memory addresses 0 to 1

serialized it should be: ``0x60FD60005360016000F3``

.. code-block:: plain

    ? Enter the calldata: 0x60FD60005360016000F3
    Puzzle solved!

😎 some day I'll figure out if not having the two arguments for the error message in the stack is
actually valid or if the internal transaction actually reverts with a stack underflow.

Puzzle 9
========

.. code-block:: plain

    00      36        CALLDATASIZE // [ len(DATA) ]
    01      6003      PUSH1 03     // [ 03 len(DATA) ]
    03      10        LT           // [ 03<len(DATA) ]
    04      6009      PUSH1 09     // [ 09 03<len(DATA) ]
    06      57        JUMPI        // [  ] -- jumped if ^
    07      FD        REVERT       // [  ]
    08      FD        REVERT       // [  ]
    09      5B        JUMPDEST     // [  ]
    0A      34        CALLVALUE    // [ VALUE ]
    0B      36        CALLDATASIZE // [ len(DATA) ]
    0C      02        MUL          // [ VALUE*len(DATA) ]
    0D      6008      PUSH1 08     // [ 08 VALUE*len(DATA)  ]
    0F      14        EQ           // [ 08==VALUE*len(DATA)  ]
    10      6014      PUSH1 14     // [ 14 08==VALUE*len(DATA) ]
    12      57        JUMPI        // [  ] -- jumped if ^
    13      FD        REVERT       // [  ]
    14      5B        JUMPDEST     // [  ]
    15      00        STOP         // [  ]

    ? Enter the value to send: (0)

I gotta find both value & calldata so that

- ``len(calldata) >= 4``
- ``len(calldata) * callvalue == 0x08``

let's try my favorite kind of case: the degenerate case. Value 1, calldata length 8:
``0xFFFFFFFFFFFFFFFF``

.. code-block:: plain

    ? Enter the value to send: 1
    ? Enter the calldata: 0xFFFFFFFFFFFFFFFF

    Puzzle solved!

``(⌐■_■)``

Puzzle 10
=========

.. code-block:: plain

    00      38          CODESIZE     // [ 1B ] --
    01      34          CALLVALUE    // [ VALUE 1B ] --
    02      90          SWAP1        // [ 1B VALUE ] --
    03      11          GT           // [ 1B>VALUE ] --
    04      6008        PUSH1 08     // [ 08 1B>VALUE ] --
    06      57          JUMPI        // [  ] --
    07      FD          REVERT       // [  ] --
    08      5B          JUMPDEST     // [  ] --
    09      36          CALLDATASIZE // [ len(DATA) ] --
    0A      610003      PUSH2 0003   // [ 0003 len(DATA) ] --
    0D      90          SWAP1        // [ len(DATA) 0003 ] --
    0E      06          MOD          // [ len(DATA)%0003 ] --
    0F      15          ISZERO       // [ len(DATA)%0003==0 ] --
    10      34          CALLVALUE    // [ VALUE len(DATA)%0003==0 ] --
    11      600A        PUSH1 0A     // [ 0A VALUE len(DATA)%0003==0   ] --
    13      01          ADD          // [ 0A+VALUE len(DATA)%0003==0 ] --
    14      57          JUMPI        // [  ] -- jumped to 0A+VALUE if length
                                     //        of calldata is divisible by 3
    15      FD          REVERT       // [  ] --
    16      FD          REVERT       // [  ] --
    17      FD          REVERT       // [  ] --
    18      FD          REVERT       // [  ] --
    19      5B          JUMPDEST     // [  ] --
    1A      00          STOP         // [  ] --

    ? Enter the value to send: (0)

- ``0A+callvalue == 19`` otherwise it won't jump to the exit JUMPDEST-> value must be 9
- ``len(CALLDATA)`` should be a multiple of 3, otherwise instruction ``14`` won't jump anywhere
- ``VALUE`` must be less or equal to ``1B`` -- superfluous considering the first restriction

.. code-block:: plain

    ? Enter the value to send: 9
    ? Enter the calldata: 0xFFFFFFFFFFFF

    Wrong solution :(

let's check the first item:

.. code-block:: plain

    0A+callvalue == 19 <=>
    callvalue==19-0A <=>
    callvalue==9 ??? no! wtf capu.
    callvalue==0d15 // better

the way I normally do this kind of operation is with ``bc``, unix's 'basic calculator'.

On the first attempt, I hda a small tpyo where I wrote ``obase=16; 19-0A``.
if you give that line to ``bc``, either interactively or with, say, ``echo "obase=16; 19-0A" |bc``,
it'll interpret the input as decimal (no idea why it doesn't crash when it sees that ``A``) and give
the output in hexadecimal. If I the calculator properly and send ``echo "ibase=16; 19-0A" |bc`` it
outputs 15 in decimal, the correct answer.

.. note::

    I have a binding:
    ``nnoremap <leader>c yypV!bc -l<cr>``
    to make this easier

.. code-block:: plain

    ? Enter the value to send: 15
    ? Enter the calldata: 0xFFFFFF

    Puzzle solved!

This should be all! Although there's something I still want to do from the first puzzle...

.. note::

    Perhaps this a reason against using qwerty? It'd be fun to see a keyboard distribution with a
    focus on minimizing problematic typos.

Bonus: get the last puzzle to loop indefinetely
===============================================
Given the puzzle executor is probably instantiating a real EVM, I'll most likely get a 'failed
puzzle' and nothing else, perhaps a slight delay if the vm is implemented in JS

going back to the bytecode:

.. code-block:: plain

    00      38          CODESIZE     // [ 1B ] --
    01      34          CALLVALUE    // [ VALUE 1B ] --
    02      90          SWAP1        // [ 1B VALUE ] --
    03      11          GT           // [ 1B>VALUE ] --
    04      6008        PUSH1 08     // [ 08 1B>VALUE ] --
    06      57          JUMPI        // [  ] --
    07      FD          REVERT       // [  ] --
    08      5B          JUMPDEST     // [  ] --
    09      36          CALLDATASIZE // [ len(DATA) ] --
    0A      610003      PUSH2 0003   // [ 0003 len(DATA) ] --
    0D      90          SWAP1        // [ len(DATA) 0003 ] --
    0E      06          MOD          // [ len(DATA)%0003 ] --
    0F      15          ISZERO       // [ len(DATA)%0003==0 ] --
    10      34          CALLVALUE    // [ VALUE len(DATA)%0003==0 ] --
    11      600A        PUSH1 0A     // [ 0A VALUE len(DATA)%0003==0   ] --
    13      01          ADD          // [ 0A+VALUE len(DATA)%0003==0 ] --
    14      57          JUMPI        // [  ] -- jumped to 0A+VALUE if length
                                     //        of calldata is divisible by 3
    15      FD          REVERT       // [  ] --
    16      FD          REVERT       // [  ] --
    17      FD          REVERT       // [  ] --
    18      FD          REVERT       // [  ] --
    19      5B          JUMPDEST     // [  ] --
    1A      00          STOP         // [  ] --

    ? Enter the value to send: (0)

..

    - ``0A+callvalue == 19`` otherwise it won't jump to the exit JUMPDEST-> value must be 15

But what if I want to jump somewhere other than ``0x19``? perhaps to ``0x08``?

The lowest I can go with the value is zero, and that would make execution jump to ``0x0A``. Which is
greater than ``0x08``. And there aren't any JUMPDESTs after that other than the 'exit' one on
``0x19``.

What if I send so much that it overflows? Well, I could find a value X such that ``0x0A+X ==
0x08``. And the EVM doesn't check for overflows, so that could work. The value would be...

.. code-block:: plain

    (X+0x0A)-max = 0x08 // it shoud really be a %, but a - is equivalent for a single overflow
    X+0x0A=0x08+max
    X=0x08+max-0x0A
    X=max-(0x0A-0x08)
    X=max-0x02


However, instruction at ``0x03`` prevents me from doing such a thing. The comparison made by opcode GT
interprets both operands as **unsigned** integers. ``type(uint).max-2`` is obviously greater than
``0x1B``. However, if only ``type(uint).max-2`` was interpreted as a *signed* integer, then, since
the first bit is 1, it'd be a negative number, and instruction at ``0x03`` would push 1 to the
stack.

In conclusion, I didn't get to break this puzzle, but I got some ideas for developing a new one.

Sorry for the spoiler, in case future me actually implemented it.

Thanks for reading!

.. [1] when trying to access the return data of a call, you have to use the RETURNDATASIZE and
   RETURNDATACOPY opcodes, they're not pushed to the stack. What *is* pushed to the stack though, is
   wether the call finished gracefully (1) or reverted (0)
