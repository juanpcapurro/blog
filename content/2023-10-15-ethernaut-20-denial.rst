###########################
Ethernaut 20: Denial
###########################
:date: 2023-10-15
:status: draft
:slug: ethernaut-20-denial
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

    contract Denial {
        address public partner; // withdrawal partner - pay the gas, split the withdraw
        address payable public constant owner = payable(address(0xA9E));
        uint256 timeLastWithdrawn;
        mapping(address => uint256) withdrawPartnerBalances; // keep track of partners balances

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


Solution
========
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1
