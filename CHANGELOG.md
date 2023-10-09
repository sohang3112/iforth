# Change Log

## [Unreleased] - 2023-09-19

### Added
- Added Forth syntax highlighting by correcting language name of Jupyter kernel.
- Supported running shell commands by prefixing with `!`.
- Added `py.typed` marker file so that mypy will use the type annotations.
- **WIP:** Added `Dockerfile` to allow building and running as `docker` containers. This is especially useful on Windows.


## [0.3] - 2023-02-21

### Fixed
- While installing, warn if `gforth` is not installed.
- Error outputs properly marked so that they are highlighted with red background in Jupyter Notebook.
- Kill the Jupyter kernel if underlying `gforth` process dies (for example, by running command `bye`).