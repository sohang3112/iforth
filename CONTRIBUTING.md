# CONTRIBUTING

## Development Installation

- Git clone this repo and `cd` to it.
- [uv](https://github.com/astral-sh/uv) automatically does editable install: `uv run python -m forth_kernel.self_install --user`.

## Publishing a new release

- Test it's working correctly.
- Increment the version number in _pyproject.toml_.
- Build source & wheel packages: `uv build`.
- Upload package to PyPi : `uv publish --token PYPI_TOKEN`.
- Make a new release on Github.
