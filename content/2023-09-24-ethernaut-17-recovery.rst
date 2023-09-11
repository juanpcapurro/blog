###########################
Ethernaut 17: Recovery
###########################
:date: 2023-09-24
:status: draft
:slug: ethernaut-17-recovery
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

    contract Recovery {
        //generate tokens
        function generateToken(string memory _name, uint256 _initialSupply) public {
            new SimpleToken(_name, msg.sender, _initialSupply);
        }
    }

    contract SimpleToken {
        // public variables
        string public name;
        mapping(address => uint256) public balances;

        // constructor
        constructor(string memory _name, address _creator, uint256 _initialSupply) {
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
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1
