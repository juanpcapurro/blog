##########################
So you want to use DSProxy
##########################
:date: 2022-3-01
:summary: Better delegate that to me \*ba dum tss*
:tags: programming, solidity
:author: capu
:featured_image:

But why?
========
Let's say you're making a *dapp* for a protocol where you can deposit your
tokens and receive interest on them.

Let's say that you also want that dapp to also swap that token from ETH, so the
user goes into the dapp with ETH and with Just One Click, ends up with exposure
to whatever the cool kids are pumping this week.

For the user, you want to provide the most streamlined experience possible:

.. uml::

   @startsalt
    {
      Interest yielding DAPP
      ---
      ^Which token^
      ---
      How much:
      "U$:     " | "   TKN"
      ---
      [ LEND ]
    }
   @endsalt

But behind the scenes, you have (actors):

- an exchange, to swap ETH for TKN
- the interest yielding protocol
- the actual token a user wants to hold

and interactions:

- swap the eth for the token
- allow the token to the interest yielding protocol
- lock the token into ^

Each interaction means the user having to sign a transaction with the wallet of
their choosing, and keeping track in the dapp of the intermediate states (If a
user already swapped eth and reloads the page, you wouldn't make them start
from the beggining, right?)

So, if you want to do all that with just one button, how do you achieve it?

Introducing DSProxy
===================
DSProxy is a contract template deployed for every user which enables them to do
several contract calls in a single transaction

It's controlled by the user, and it's meant to 'represent' them in some
capacity (eg: hold their token balances)

It has little functionality on its own, and instead delegates it to separate
implementation contracts

How it works
============
Following the aforementioned example, you'd need:

- The user having their own DSProxy contract. For now we'll assume they already have one.
- An actual implementation contract which defines what calls will the proxy will actually make

.. uml::

    Participant EOA
    Participant TKN
    Participant DSProxy
    Participant Implementation
    Participant Exchange
    Participant "Yield Protocol"

    EOA -> DSProxy: execute(implAddress, calldata)
    Note right: this is a regular call. there are\n no delegatecalls from EOAs\nmsg.sender: EOA
    DSProxy -> Implementation: whateverCalldataSaid
    Note right: this is a delegatecall\nmsg.sender: EOA
    Implementation -> Exchange: swapWithEth(...)
    Note right: this is a regular call\nmsg.sender: DSProxy\nTKNs will be sent to DSProxy
    Implementation <-- Exchange
    Implementation -> TKN: approve(yieldProtocolAddress,amount)
    Implementation <-- TKN
    Implementation -> "Yield Protocol": lend
    Implementation <-- "Yield Protocol"
    DSProxy <-- Implementation
    EOA <-- DSProxy

But the user's address wouldn't ever hold TKNs!
-----------------------------------------------
...or the tokens that ``lend`` would create, if any. That's correct. Ideally
the dapp should know to use the tokens held by the user's DSProxy, and enable
the user to move the tokens from there to their actual wallet.

But why not make a ``delegateCall`` to ``Exchange``, ``Token`` or ``Yield Protocol``?
-------------------------------------------------------------------------------------
That looks tempting, so ``msg.sender`` would be the EOA and tokens would
be minted to the user directly, right?

It's correct that ``msg.sender`` would be the EOA, but calling the different
protocol contracts (eg, the ``Exchange``) most certainly wouldn't do what you
expect.

When calling for example the ``TKN`` token, you *want* to use that
contract's storage in the call and modify it, since that's where the balances
are actually stored. Running an ERC20's contract code on a DSProxy storage is
almost C-style undefined behaviour.

How do I know the DSProxy does a delegateCall to the implementation?
--------------------------------------------------------------------
First: `the code
<https://github.com/dapphub/ds-proxy/blob/e17a2526ad5c9877ba925ff25c1119f519b7369b/src/proxy.sol#L64>`_
, but also, the existence of the DSCache, a contract that skips deployment of
an implementation contract if the same bytecode was already deployed in the
past, shows that the implementation's contract storage is not used.

Further reading
===============
- DSProxy code: https://github.com/dapphub/ds-proxy
- Solidity's delegateCall documentation (overview): https://docs.soliditylang.org/en/v0.8.4/introduction-to-smart-contracts.html?highlight=delegatecall#delegatecall-callcode-and-libraries
- docs for Solidity's inline assembly directive for ``delegateCall`` https://docs.soliditylang.org/en/v0.8.4/yul.html#yul-call-return-area
- The `Ethereum yellow paper <http://gavwood.com/paper.pdf>`_ in page 30 specs the delegatecall opcode. I understood like 5% of it.

Notes
=====
- DSProxy is not the only way to achieve this, another example is Gnosis Contract Proxy Kit
- I haven't written an actual POC on this, so if it reads like I'm talking out of my ass, it's because that's the case.
