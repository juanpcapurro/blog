#######################################
Updates to solhint-community versioning
#######################################
:slug: updates-to-solhint-community-versioning
:date: 2023-07-24
:status: draft
:summary: Sorry for all those false positives. This should mitigate it.
:tags: programming
:author: capu
:featured_image:

TL;DR
=====
There's a pre-release version of solhint-community: ``3.7.0-rc00``. Please use
it and report issues on the new rules if you find any!

Context
-------

I've been maintaining `solhint-community
<https://github.com/solhint-community/solhint-community/pulls>`_ for a few weeks
now, and shipped two new rules:

- no-unused-import
- named-parameters-function

However, the former's initial implementation was way buggier than I could
anticipate. As far as I could tell, the project has three users [1]_ :

- whatever `0xCourtney <https://github.com/0xCourtney>`_ is working on
- the `sablier labs <https://github.com/sablier-labs/>`_ organization
- the `prb repos <https://github.com/PaulRBerg/>`_

They all reported false positives on the no-unused-import rule. And plenty of
them, too!

- `False positive when using a type in a mapping value <https://github.com/solhint-community/solhint-community/issues/28>`_
- `False positive when using a type in inheritdoc <https://github.com/solhint-community/solhint-community/issues/31>`_
- `False positive when using a type in using...for <https://github.com/solhint-community/solhint-community/issues/29>`_
- `False positive when using a type's creation code <https://github.com/solhint-community/solhint-community/issues/20>`_
- `False positive when using an imported constat <https://github.com/solhint-community/solhint-community/issues/19>`_
- `False positive when using a type in an override modifier <https://github.com/solhint-community/solhint-community/issues/17>`_

In retrospect, it makes sense this happened. Like most people, I didn't use
*every* language feature, even after a few years on it, and I haven't programmed
solidity significantly since a few releases ago. Plus I probably have enough
fingers to count how many trees like this one I've significantly walked 🙃.

While I learned a lot in the process, I'm not naive enough to assume these are
all the mistakes I'm ever going to make. So I should have some mitigations
against them.

What I'm going to do about it
=============================
This is a bit of an 'unknown unknowns' problem. I won't be finding many bugs if
I don't get free QA from users stumbling on issues I didn't anticipate. But I
don't want users to have a bad experience using the linter I maintain either!
They're users. They didn't sign up to help me develop the thing.

But what if they did?

Introducing pre-release versions
--------------------------------
`semantic versioning <https://semver.org/>`_ has the concept of pre-release
versions, which look like this: ``mayor.minor.patch-preReleaseIdentifier``.
The idea with this is users can sign up to receive features some time before
they make it into a new version by using a pre-release for it. (These are also
known as release candidates, or rc for short)

npm  has `sensible defaults <https://docs.npmjs.com/cli/v6/using-npm/semver>`_
for this. Basically:

- If you sign up for pre-release version ``^1.2.3-rc01``, you'll get all the
  pre-releases for version ``1.2.3`` which have a pre-release identifier greater
  (lexicographically) than ``rc01``, plus any proper releases greater than
  ``1.2.3`` that don't imply a major version change, such as ``1.4.0``

when in doubt, you can use ``semver`` as a command line utility to check which
versions match a particular range:

.. code-block:: fish

    [I] capu ~/s/blog (master)> semver --range '^1.2.3-rc01'\
    1.2.3-rc00 1.2.3-beta 1.2.3-rc01 1.2.3-zeta 1.2.3-rc02 1.4.0

    1.2.3-rc01
    1.2.3-rc02
    1.2.3-zeta
    1.4.0

An invitation to try solhint-community 3.7.0
============================================
solhint-community ``3.6.0`` is already out, so any bugs with it will be
fixed on patch versions to it.

However, I'm creating a release candidate ``3.7.0-rc00`` for the next minor version,
alongside a branch called ``release-candidate-3.7.0`` to which new rules and/or
other changes that merit a minor version release will be merged.

So, please feel free to use the ``^3.7.0-rc00`` version range in your
package.json to get new rules as soon as possible. For a few repos I think I'll
just post a PR and see what the owners think.

The idea, which for now is taken from VDD (Vibes Driven Development) theory, is
to be one order of magnitude more sure about the absence of bugs to merge
something to the ``master`` branch (and shortly after release it) than to merge
something to a release candidate branch.

Happy lintin'!


.. [1] there's no telemetry on solhint (and there won't be) so I have no way of
   knowing who uses it other than people telling me or reporting issues, and I
   can only have an overview on how many users it has based on how many times
   it's downloaded from npm. So of course it'll look like everyone using it is
   having issues.
