# Change Log

## [Unreleased] - 2023-09-19

### Added
- Add Forth syntax highlighting by correcting language name of Jupyter kernel.
- In Jupyter cell output, highlighted actual code output in bold (as opposed to where `gforth` is just echoing the input code).
- Support running shell commands by prefixing with `!`.
- Add `py.typed` marker file so that mypy will use the type annotations.
- **WIP:** Add `Dockerfile` to allow building and running as `docker` containers. This is especially useful on Windows.


## [[0.3] - 2023-02-21](https://github.com/sohang3112/iforth/releases/tag/v0.3)

### Fixed
- While installing, warn if `gforth` is not installed.
- Error outputs properly marked so that they are highlighted with red background in Jupyter Notebook.
- Kill the Jupyter kernel if underlying `gforth` process dies (for example, by running command `bye`).