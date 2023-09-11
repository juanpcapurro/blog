###########################
Ethernaut 19: AlienCodex
###########################
:date: 2023-10-18
:status: draft
:slug: ethernaut-19-aliencodex
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

    contract AlienCodex is Ownable {
        bool public contact;
        bytes32[] public codex;

        modifier contacted() {
            assert(contact);
            _;
        }

        function make_contact() public {
            contact = true;
        }

        function record(bytes32 _content) public contacted {
            codex.push(_content);
        }

        function retract() public contacted {
            codex.length--;
        }

        function revise(uint256 i, bytes32 _content) public contacted {
            codex[i] = _content;
        }
    }


Solution
========
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 1
