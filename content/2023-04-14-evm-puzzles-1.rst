###########################
Let's play some EVM Puzzles
###########################
:date: 2023-04-14
:summary: omg manually following processor instructions hiiii
:tags: programming
:slug: evm-puzzles-1
:author: capu
:featured_image:

`EVM Puzzles <https://github.com/fvictorio/evm-puzzles>`_ is a game dealing
with EVM assembly, where you have to provide calldata and/or call value to get
a contract call to execute successfully. It's inspired by `Overthewire's
wargames <https://overthewire.org/wargames/>`_ , which are a lot of fun.

This should be the first in a series. Ideally I both show you how to solve them
and also showcase my brainfarts and false starts.

Puzzle 1
========

.. code-block:: plain

    00      34      CALLVALUE
    01      56      JUMP
    02      FD      REVERT
    03      FD      REVERT
    04      FD      REVERT
    05      FD      REVERT
    06      FD      REVERT
    07      FD      REVERT
    08      5B      JUMPDEST
    09      00      STOP

    ? Enter the value to send:

'I like your magic columns, funny man', you might comment.

Let's dive into what the three columns mean. Take the second one as an example:

.. code-block:: plain

    01      56      JUMP

- ``01`` is the offset of the current instruction from the beggining of the
  bytecode. you could think of it as an array's index. It starts at zero, and
  is noted in hexadecimal.
- ``56`` this is the opcode itself. The ``PUSH`` opcodes are longer than 1
  byte, because they include the value that they'll push onto the stack. This
  will cause some jumps in the value of the first column.
- ``JUMP`` is the human-readable representation of the opcode, for the
  unreliable flesh-puters in our heads.

assembly is usually annotated with two more items:

- ``[stack1 stack2]`` expected stack state after executing the instruction
- other comments in good ol' human-speak.

with this, you can interpret the following

for reference on the available opcodes, you can visit `evm.codes
<https://evm.codes>`_ . It even has a line-by-line debugger!

.. code-block:: plain

    00      34      CALLVALUE // [ VALUE ] push the callvalue onto the stack
    01      56      JUMP      // [] jumped to index VALUE
    02      FD      REVERT
    03      FD      REVERT
    04      FD      REVERT
    05      FD      REVERT
    06      FD      REVERT
    07      FD      REVERT
    08      5B      JUMPDEST
    09      00      STOP

the contract will jump to whatever value I send. And I want it to jump to index
``08``.

.. code-block:: plain 

    ? Enter the value to send: 8

    Puzzle solved!

success!

I find it fun to break things, so when something jumps to whatever I tell it
to, I wonder: can I make it go back, *unconditionally?*. That'd cause an
infinite loop.

.. code-block:: plain

    ? Enter the value to send: 0

    Wrong solution :(

Answer is no in this case. And we have the ``JUMPDEST`` opcode to thank for
that. When JUMPing, the EVM will check the destination and revert if the
there is something other than a ``JUMPDEST`` opcode. Neat.

.. note::

    my favorite bad way to explain Ethereum is 'it's just like bitcoin, but you
    have an opcode to jump *wherever*! even *backwards*!'

Puzzle 2
========

.. code-block:: plain

    00      34      CALLVALUE // [VALUE]
    01      38      CODESIZE  // [09 VALUE]
    02      03      SUB       // [ 09-VALUE ]
    03      56      JUMP      // [  ] jumps to (09-VALUE)
    04      FD      REVERT
    05      FD      REVERT
    06      5B      JUMPDEST
    07      00      STOP
    08      FD      REVERT
    09      FD      REVERT

answer seems to be to find a value such that ``09-VALUE==06``

I can deal with that 😎

.. code-block:: plain

    ? Enter the value to send: 3

    Wrong solution :(

what? is my math wrong?

surprisingly no, my math was okay. Thing is, the last bytecode has index
``09``. But indexing starts at zero. So the bytecode has length 10. ``0x0A``,
in computer words.

``0A-VALUE==06`` means I should send a value of 4.

.. code-block:: plain

    ? Enter the value to send: 4

    Puzzle solved!

``(⌐■_■)``

Puzzle 3
========

.. code-block:: plain

    00      36      CALLDATASIZE // [len(DATA)]
    01      56      JUMP         // jumped to len(DATA)
    02      FD      REVERT
    03      FD      REVERT
    04      5B      JUMPDEST
    05      00      STOP

I should send some data as long as it has a length of... 4.

remember each byte is represented by two characters ``0-F``:

.. code-block:: plain

    ? Enter the calldata: 0xFFFFFFFF

    Puzzle solved!

``(⌐■_■)``

Puzzle 4
========

.. code-block:: plain

    00      34      CALLVALUE // [ VALUE ]
    01      38      CODESIZE  // [ 0C VALUE ] -- remember, the lenght, not the last index
    02      18      XOR       // [ 0CXVALUE ]
    03      56      JUMP      // jumped to 0CXVALUE
    04      FD      REVERT
    05      FD      REVERT
    06      FD      REVERT
    07      FD      REVERT
    08      FD      REVERT
    09      FD      REVERT
    0A      5B      JUMPDEST
    0B      00      STOP

I need to provide a value such that ``0C XOR VALUE == 0A``

my first approach was solve for it bit by bit:

.. code-block:: plain

    0C 0000 1100
    ?? ???? ????
    ============
    0A 0000 1010

But then I remembered: if ``A XOR B == C``, then ``A XOR C == B``

so:

.. code-block:: plain

    0C 0000 1100
    0A 0000 1010
    ============
    06 0000 0110

.. code-block:: plain

    ? Enter the value to send: 6

    Puzzle solved!

yey.

Puzzle 5
========

.. code-block:: plain

    00      34          CALLVALUE  // [ VALUE ]
    01      80          DUP1       // [ VALUE VALUE ]
    02      02          MUL        // [ VALUE*VALUE ]
    03      610100      PUSH2 0100 // [ 0100 VALUE*VALUE ]
    06      14          EQ         // [ 0100==VALUE*VALUE ]
    07      600C        PUSH1 0C   // [ 0C 0100==VALUE*VALUE ]
    09      57          JUMPI      // jumps to 0C if 0100==VALUE*VALUE
    0A      FD          REVERT
    0B      FD          REVERT
    0C      5B          JUMPDEST
    0D      00          STOP
    0E      FD          REVERT
    0F      FD          REVERT

I gotta find a value that, squared, is ``0x0100``

``0x0100==0d256`` ; ``sqrt(256) == 16.00000000000000000000``

when I typed ``0x10``, however, my response was parsed as zero.

.. code-block:: plain

  ? Enter the value to send: 0

  Wrong solution :(

Turns out the value is always parsed with base 10. Fun that I managed to get
this far without realizing it.

.. code-block:: plain

  ? Enter the value to send: 16

  Puzzle solved!

Okay this is all for now. Tune in sometime between tomorrow and June 2026 for
the rest of the puzzles! 
