###########################
Ethernaut 21: Shop
###########################
:date: 2023-10-22
:status: draft
:slug: ethernaut-21-shop
:summary: TODO
:tags: 
:author: capu
:featured_image:


Objective
=========

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1

    interface Buyer {
        function price() external view returns (uint256);
    }

    contract Shop {
        uint256 public price = 100;
        bool public isSold;

        function buy() public {
            Buyer _buyer = Buyer(msg.sender);

            if (_buyer.price() >= price && !isSold) {
                isSold = true;
                price = _buyer.price();
            }
        }
    }


Solution
========
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1

    foo
