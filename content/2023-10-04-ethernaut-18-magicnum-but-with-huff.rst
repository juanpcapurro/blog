##################
Let's try out huff
##################
:date: 2023-10-04
:slug: 2023-10-04-huff
:summary: let's over-engineer my last post until it's not fun anymore
:tags: programming
:author: capu
:featured_image:

my excuse
=========

In `my last blog post <{filename}/2023-10-01-ethernaut-18-magicnum.rst>`_ I
solved Ethernaut's `MagicNum challenge
<https://ethernaut.openzeppelin.com/level/18>`_ , where the objective is to
hand-craft a very simple contract (only required to return the number 42) in
bare assembly (since it's required to be 10 bytes long or less).

To actually construct the assembly, I simply did it by hand looking up
`evm.codes <https://www.evm.codes/>`_ where necessary. It was a bit painful to
have to count bytes each time I wanted to change something or having to look
up/remember the hexadecimal representation of any opcode I wanted to use.

The thing is, it doesn't have to be like that. Assemblers have existed
for the longest time to not have to write all of the program by hand in
hexadecimal notation.

That's where `huff <https://docs.huff.sh/>`_ comes in! 

But capu, you might say, didn't solidity ship with an assembly language called
``yul``? I mean you used it to actualy deploy your handcrafted bytecode just a
few days ago:

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

Well, made-up interlocutor, you're kinda right in the sense that's a lower level
representation, but it's not exactly what I want. Yul abstracts away stack
management (there's no way of putting a ``PUSH`` or ``DUP`` instruction manually) and
control flow (it uses 'normal' looping and if constructs and has no way to
manually put a ``JUMPI``/``JUMPDEST`` instruction)

what is huff anyway?
====================
huff is an assembly language closer to the metal, similar to writing opcodes by
hand, which gives me greater control on how many and which opcodes will actually
be used, so it's better suited for this.

After a quick peek at `the tutorial
<https://docs.huff.sh/tutorial/the-basics/>`_ and piping the contents of some
url into the sanctity of my shell, I was able to compile a small hello world
program into bytecode with a bare ``huffc``. 

But that's not enough! I still have to deploy it from my tests. which would
involve:

- ``FFI`` ing the ``huffc`` command to compile the file I want
- parsing the output of ^ into some useful representation
- deploying it to the EVM, which would involve the exact same yul assembly block
  as above.

Since I seem to be on an `abstracting mood
<https://en.wikipedia.org/wiki/Cowardice>`_ , I'll also use the `foundry-huff
<https://github.com/huff-language/foundry-huff>`_ library to hide this
complexity somewhere else as well.

After adding the library to ``lib/`` and enabling ``ffi`` on ``foundry.toml``,
I'm ready to define the solver contract in huff:

.. code-block:: plain

    #define macro MAIN() = {
        0x2a 0x1f mstore8
        0x20
        0x00
        return
    }

and integrate the library like into the test contract like so

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 10

    import {HuffDeployer} from "foundry-huff/HuffDeployer.sol";

    // ...

    function solution(address payable target_) internal override {
        MagicNum target = MagicNum(target_);

        address deployment = HuffDeployer.deploy("magicnum");
        target.setSolver(deployment);
        vm.startPrank(attacker, attacker);
    }

Some :strike:`complaints` details
---------------------------------
I found some issues when using huff, namely

- I had to put the assembly file in ``src/magicnum.huff``. I tried to locate it
  under ``test/`` but it was impossible since `it's hardcoded in foundry-huff
  that they'll be found there
  <https://github.com/huff-language/foundry-huff/blob/main/src/depreciated/StatefulDeployer.sol#L50>`_ .
  Not a big deal. I rather have to deal with this than wrap my head around
  some ``remappings-but-for-huff.txt``. However, the error messages that I got for
  placing it in the wrong location were generically uttered by foundry's
  ``vm.ffi`` and not by foundry-huff in a particularly useful way. Perhaps I
  could try submitting a PR with better error handling?
- see that ``vm.startPrank``? well I had to add it because the `deployer
  contract starts a prank and never stops it
  <https://github.com/solhint-community/solhint-community/pull/41>`_ and that
  was causing my solution to fail, not because the assembly was wrong, but
  because when checking the solution with the Ethernaut contract, ``msg.sender``
  was not the attacker. I'll probably create an issue for this, since there
  might be something that I'm not getting.

Also, when playing around with all this I discovered `the disassembler I like
<https://github.com/crytic/pyevmasm>`_ doesn't support the ``PUSH0`` opcode. But
that's kinda off-topic.

See you this sunday for the solution to the (in my opinion) second-best
ethernaut CTF
