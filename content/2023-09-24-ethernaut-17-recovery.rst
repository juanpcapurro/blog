###########################
Ethernaut 17: Recovery
###########################
:date: 2023-09-24
:slug: ethernaut-17-recovery
:summary: omg protocol spec hiiii ✨
:tags: programming
:author: capu
:featured_image:


Objective
=========
Recover or remove the ETH balance sent to a SimpleToken created with the
Recovery contract.

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 7

    contract Recovery {
        //generate tokens
        function generateToken(
            string memory _name,
            uint256 _initialSupply
        ) public {
            new SimpleToken(_name, msg.sender, _initialSupply);
        }
    }

    contract SimpleToken {
        // public variables
        string public name;
        mapping(address => uint256) public balances;

        // constructor
        constructor(
            string memory _name,
            address _creator,
            uint256 _initialSupply
        ) {
            name = _name;
            balances[_creator] = _initialSupply;
        }

        // collect ether in return for tokens
        receive() external payable {
            balances[msg.sender] = msg.value * 10;
        }

        // allow transfers of tokens
        function transfer(address _to, uint256 _amount) public {
            require(balances[msg.sender] >= _amount);
            balances[msg.sender] -= _amount;
            balances[_to] = _amount;
        }

        // clean up after ourselves
        function destroy(address payable _to) public {
            selfdestruct(_to);
        }
    }

Solution
========
This is another one where there are lots of ways to cheat. I want to learn as
much as possible, so I'll abstain from the easy ways, such as using ``forge test
-vvv --mc Recovery`` (locally), using an explorer (if playing on a testnet), or
reading the ``RecoveryFactory`` source code.


How to recover the funds
------------------------
Recovering the funds, given the contract address, is simply a matter of calling
the ``selfdestruct`` method. The real problem, then, lies in finding the
address.

Finding the address
-------------------
The address a contract will be deployed to, like everything in Ethereum's
execution layer, is very well defined in the yellowpaper:

    The address of the new account is defined as being the
    rightmost 160 bits of the Keccak-256 hash of the RLP
    encoding of the structure containing only the sender and
    the account nonce

.. note::

    keep in mind there are two opcodes to deploy a contract, CREATE, and
    CREATE2. This post is concerned with the former, which is the one used by a
    good ol' ``new`` creation. 

so something like this...

.. code-block:: solidity

    rightmost160bits(
        keccak256(RLP(concatenate(
            sender,
            nonce
        )))
    )

hold on, what is RLP?
---------------------

It means Recursive Length prefix, and there are two places where I found info
about it: Appendix B of the yellowpaper and `this neat little page under
ethereum.org
<https://ethereum.org/en/developers/docs/data-structures-and-encoding/rlp/>`_.

It's an encoding with the purpose of serializing two data types: 'strings' and
arrays (which can be empty, contain strings, or other arrays). Strings in this
context mean something more akin to ``bytes`` in solidity, meaning just an
arbitrary sequence of bytes.

.. note::

    It's a really bare-bones protocol, not providing different 'leaf' data types or
    dictionaries natively. This means, if you want to send something more
    complex over it, you'll kind of have to make another protocol on top of it

The Ethereum.org defines 5 cases, for this explaination I'll BFS through them as
needed:

- strings:
    - A single byte whose value is in the [``0x00``, ``0x7f``] (decimal [0, 127]) range.
    - Otherwise, a string 0-55 bytes long
    - A string more than 55 bytes long, 
- lists:
    - A list with a total payload (i.e. the combined length of all its items
      being RLP encoded) between 0-55 bytes long.
    - A list with a total payload longer than 55 bytes

I have to RLP encode two items, so that's a list. It'll probably not be longer
than 55 bytes, since addresses are 20 bytes and the nonce is likely a low
number.

.. note::

    the RLP spec forbids sending leading zeros when the 'string' is an integer,
    so that tells me I should not send the 32 bytes used for the nonce in the
    EVM, and only send as many bytes as necessary to represent the number
    instead.

..

    A list with a total payload  between 0-55 bytes long.
        the RLP encoding consists of a single byte with value ``0xc0`` plus the
        length of the payload followed by the concatenation of the RLP encodings
        of the items. The range of the first byte is thus [``0xc0,`` ``0xf7``] (dec.
        [192, 247])

so the first byte is ``0xc0`` plus the length of the payload, which I do not
know yet

.. code-block:: solidity

    bytes memory rlpEncode = bytes.concat(
        bytes1(uint8(0xc0)+uint8(/*??*/))
        /*???*/
    );

The payload, in turn, is the address and the nonce

The address is a 20-byte string. That fits between 0 and 55, so

    Otherwise, a string 0-55 bytes long
        the RLP encoding consists of a single byte with value ``0x80`` (dec. 128)
        plus the length of the string followed by the string. The range of the
        first byte is thus [``0x80``, ``0xb7``] (dec. [128, 183])

then, the first byte of the payload is ``0x80`` plus ``0x14`` (decimal 20), and
the following 20 bytes are the address

.. code-block:: solidity

    bytes memory rlpEncode = bytes.concat(
        bytes1(uint8(0xc0)+uint8(/*??*/))
        bytes1(uint8(0x80)+uint8(0x14)),
        bytes20(address(targetAddress)),
        /*nonce*/
    );

the nonce should come after that.

.. note::

    'Nonce' is one of those broad concepts that mean different things in
    different contexts, but all of them have the same vibe, sort of?

    In the context of an ethereum account, there are two cases

    - the account is externally owned: it's simply the number of transactions
      broadcasted by the account
    - the account is a contract: it's the amount of contracts the contract has
      deployed.

Knowing the nonce of the Recovery contract is easy because it only ever
deployed one contract. I cannot affirm or deny that when first implementing the
solution I tried 0 and 2 as well, though.

And following the note above, I'll represent it with the smallest possible type,
which is ``bytes1``. But what's the rlp encoding of ``bytes1(1)``?

    A single byte whose value is in the [``0x00``, ``0x7f``] (decimal [0, 127]) range.
        that byte is its own RLP encoding

Awesome!

.. code-block:: solidity

    bytes memory rlpEncode = bytes.concat(
        bytes1(uint8(0xc0)+uint8(/*??*/))
        bytes1(uint8(0x80)+uint8(0x14)),
        bytes20(address(targetAddress)),
        bytes1(uint8(1))
    );

The only thing left is to compute the length of the top-level list in order to
add it to the first byte. 1(address header) + 20(address) + 1(nonce) is 22,
``0x16``

Tying it all up, then:

.. code-block:: solidity

    function solution(
        address payable targetAddress
    ) internal override{
        bytes memory rlpEncode = bytes.concat(
            bytes1(uint8(0xc0)+uint8(0x16)),
            bytes1(uint8(0x80)+uint8(0x14)),
            bytes20(address(targetAddress)),
            bytes1(uint8(1))
        );
        bytes32 hashOutput = keccak256(rlpEncode);
        address firstDeployAddress = address(
            bytes20(hashOutput << 12*8)
        );
        SimpleToken(payable(firstDeployAddress))
            .destroy(payable(this));
    }
