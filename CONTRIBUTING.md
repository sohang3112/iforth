# CONTRIBUTING

## Development Installation

- Git clone this repo and `cd` to it.
- [uv](https://github.com/astral-sh/uv) automatically does editable install: `uv run python -m forth_kernel.self_install --user`.
- Run tests: `uv run --group test python tests/test_forth_kernel.py`

## Contributing a Pull Request

- Fork this Github repo, and make your desired code changes there.
- Verify your changes work correctly by manual testing.
- Add automated tests to appropriate existing or new test file in [tests/](tests/) folder. This project uses [`unittest` library](https://docs.python.org/3/library/unittest.html) to write tests.
- Run all existing and newly added automated tests.
- Raise a PR, mentioning type of change (eg. BUGFIX, FEATURE), and exactly what you improved. Check open issues, and mention which (if any) issue numbers are fixed by your PR.

## Publishing a new release

NOTE: This is for the repo maintainer to do. If you are an external contributor to this repo, you can ignore this - instead check the section [Contributing a Pull Request](#contributing-a-pull-request).

- Test it's working correctly.
- Increment the version number in _pyproject.toml_.
- Build source & wheel packages: `uv build`.
- Upload package to PyPi : `uv publish --token PYPI_TOKEN`.
- Make a new release on Github.
