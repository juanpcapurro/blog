######################################
solhint-community devlog: October 2023
######################################
:date: 2023-10-18
:slug: solhint-community-devlog-october-2023
:summary: after a short hiatus, I'm pushing versions again!
:tags: programming
:author: capu
:featured_image:

What's going on
===============

I've been grinding through some other stuff these past few weeks, during which
protofire/solhint resumed development.

While this is of course welcome, and I'm flattered my efforts pushed them to
assign some resources to the project, I'll continue working on
solhint-community for the following reasons:

- It's good practise for my language-fu
- I started the project to provide a linter to the community with a regular
  release cycle, independently of protofire's budget allocations, which have
  proven inconsistent in the past.
- It's a good way to find other issues which serve as a wedge to `get into some
  weird edge cases of the language
  <https://forum.soliditylang.org/t/interface-implementations-should-have-the-same-parameter-names-as-the-interface/1725>`_ 
- I have a different vision of how a few things should be implemented than
  protofire's current team. 

The last point is a bit contentious so I'll be more specific:

Versioning
----------

I want to take `semantic versioning
<{filename}/2023-07-24-solhint-versions.rst>`_ more seriously. I consider it a
bug to add a rule to the recommended ruleset in a patch version, for example,
since that'd mean users with a ``^`` matcher on their package.json would start
getting errors reported on their codebase just by doing an ``npm install``

Configuration
-------------

I want to take a more opinionated approach to rules & configuration, sacrificing
low degrees of configurability for high degrees of simplicity & clarity. An
example of this is the `explicit-types rule
<https://github.com/solhint-community/solhint-community/pull/41>`_ which is
where I first broke config file compatibility over an arguably petty difference:
The rule originally allowed configuration to use implicit or explicit types
(think ``uint`` vs ``uint256``).

But I think most people using a rule called explicit-types would expect it to
enforce explicit types be used, and I didn't see anyone *asking* for a rule to
enforce only implicit types are used. So I just removed the option.

A similar thing happened with `immutable-vars
<https://github.com/solhint-community/solhint-community/pull/54/commits/ea34887d35df88df1e2c89e8043068e6a72df9c2>`_
, which included a config parameter called ``immutableAsConstants`` which when
set to false enforced ``immutable`` variables to be named in ``camelCase`` like
regular variables and **not** use ``snake_case``. I chose to just remove it and
enforce immutables have names written in ``CAPITALIZED_SNAKE_CASE``.

Having this happen twice in the relatively short list of features I backported
shows there's a design difference between the two projects.

What's going to happen going forward
====================================

v3.*.*
------

I'm gonna see the little amount of users this project has as an advantage to
break compatibility with protofire/solhint (but not with solhint-community's own
semantic versioning) and continue the current trend of development.

version 3.7.0 should drop (no longer be a release candidate) some time this week
or the following.

v4.*.*
------

My focus with this version is to have a reasonable and usable default and
recommended config, and get rid of most of the deprecated stuff that has been
accumulating on the codebase for staying in v3 for so long. There's the
``breaking-change`` tag in the repo for this, and off the top of my head I can
recall:

- `merging no-unused-import and no-unused-var
  <https://github.com/solhint-community/solhint-community/issues/23>`_  which
  should also fix the issue with `the no-unused-import not recognizing an unused
  import when the name is shadowed
  <https://github.com/solhint-community/solhint-community/issues/24>`_ 
- Deleting all the deprecated rules
- Deleting or overriding the ``default`` ruleset
- merge various naming rules, such as the one for constants and the one for
  immutables.
- Re-defining which rules should be ``recommended``.

I'll drop a release candidate for this before the end of year, but I can't
promise it'll reach 'stable' status that soon.

What can you do
===============

Right now the most valuable thing I can get regarding this project is users who
submit issues for bugs.

Install ``solhint-communit@3.7.0-rc01`` to get the latest updates and not just
find some wording issue in the backyard, but take it to the deepest corner of
the language's spec basement, throw some ``using global for`` statements at it,
shoot it with the most obscure but valid syntax, try to integrate it into the
most fringe of editors, sprinkle a little flame war about a new rule for usages
of function pointers, and make a PR for a third party project to use the
unstable version after that. In 10 days we'll have the best linter in existence.
