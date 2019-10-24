
============
Contributing
============

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

The following sections detail a variety of ways to contribute,
as well as how to get started.

Types of Contributions
=======================

Write Documentation
--------------------
``pandas-log`` could always use more documentation,
whether as part of the official ``pandas-log`` docs, in docstrings, or the examples gallery.

During sprints, we require newcomers to the project to
first contribute a documentation fix before contributing a code fix.
Doing so has numerous benefits:

1. You become familiar with the project by first reading through the docs.
2. Your documentation contribution will be a pain point that you have full context on.
3. Your contribution will be impactful because documentation is the project's front-facing interface.
4. Your first contribution will be simpler, because you won't have to wrestle with build systems.
5. You can choose between getting set up locally first (recommended), or instead directly making edits on the GitHub web UI (also not a problem).
6. Every newcomer is equal in our eyes, and it's the most egalitarian way to get started (regardless of experience).

Remote contributors outside of sprints and prior contributors
who are joining us at the sprints need not adhere to this rule,
as a good prior assumption is that you are a motivated user of the library already.
If you have made a prior pull request to the library,
we would like to encourage you to mentor newcomers in lieu of coding contributions.

Documentation can come in many forms. For example, you might want to contribute:

- Fixes for a typographical, grammatical, or spelling error.
- Changes for a docstring that was unclear.
- Clarifications for installation/setup instructions that are unclear.
- Corrections to a sentence/phrase/word choice that didn't make sense.
- New example/tutorial notebooks using the library.
- Edits to existing tutorial notebooks with better code style.

In particular, contributing new tutorial notebooks and
improving the clarity of existing ones are great ways to
get familiar with the library and find pain points that
you can propose as fixes or enhancements to the library.

Report Bugs
------------
Report bugs at https://github.com/eyaltrabelsi/pandas-log/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
---------
Look through the GitHub issues for bugs.
Anything tagged with ``bug`` and ``available to hack on`` is open to
whoever wants to implement it.

Do be sure to claim the issue for yourself by indicating,
"I would like to work on this issue."
If you would like to discuss it further before going forward,
you are more than welcome to discuss on the GitHub issue tracker.


Submit Feedback
-----------------
The best way to send feedback is to file an issue at https://github.com/eyaltrabelsi/pandas-log/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)





Get Started!
====================

Ready to contribute? Here's how to set up ``pandas_log`` for local development.

1. Fork the `pandas_log` repo on GitHub: https://github.com/eyaltrabelsi/pandas-log.

2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pandas_log.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pandas_log
    $ cd pandas_log/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 pandas_log tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Pull Request Guidelines
----------------------
Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.



Deploying
---------
A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
