# MAINTAINERS

This has helpful information for the repo maintainers.

## Reviewing & Merging a Pull Request (PR)

Setup Github CLI (install it and run `gh auth login`): https://docs.github.com/en/github-cli/github-cli/quickstart .
External PR contributors' branches are in their own forks, not in this repo, so Github CLI is the easiest way to locally checkout their branches.

- Locally checkout the PR branch with: `gh pr checkout {pr_number}`.
- Do PR review & merge as usual.

## Publishing a new release

- Test it's working correctly.
- Increment the version number in _pyproject.toml_.
- Build source & wheel packages: `uv build`.
- Upload package to PyPi : `uv publish --token PYPI_TOKEN`.
- Make a new release on Github.
