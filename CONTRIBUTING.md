# Contributing Guidelines

1. Report your full operating system details, python version and
   terminal/console program and version (if applicable).
2. Ensure that your commit messages follow [these
   guidelines](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
3. Stick to the existing coding style.
4. Make sure all tests pass when run with
   [tox](https://tox.readthedocs.io/en/latest/) (missing interpreters are ok)
   and on [GitHub Actions](https://github.com/MisanthropicBit/colorise/actions).
5. Make sure linting passes `tox -e lint`.
6. Make sure all scripts/examples pass `tox -e scripts`.
7. Make sure to update the documentation if necessary and that it
   builds (run `make html` in the [docs](/docs) folder or `tox -e docs`).

## Contributing to Tested Systems

If you want to help test colorise on a new system (see [this
list](https://colorise.readthedocs.io/en/latest/tested_systems.html) for
currently tested systems), run the [tests](/tests) etc. as described above. Then please
submit a [pull request](https://github.com/MisanthropicBit/colorise/pulls) and
provide the following details.

1. Full details of the terminal/console you tested on.
2. Full details of the operating system you tested on.
3. The Python version you used for the test (make sure it is a version actually
   [supported by colorise](https://pypi.org/project/colorise/)).
4. Does `colorise.num_colors()` return the correct color count?
