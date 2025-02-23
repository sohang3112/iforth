# IForth

Forth kernel for Jupyter notebook / lab. This is a fork of [github.com/jdfreder/iforth](https://github.com/jdfreder/iforth).

[Open in Colab](https://colab.research.google.com/github/sohang3112/iforth/blob/master/forth_jupyter_tour.ipynb)

![Example Notebook Screenshot](notebook_screenshot.png)

**Note:** Check the [changelog](CHANGELOG.md) to see the latest changes in development as well as in releases.

## Installation

Install `python` and `gforth`, ensuring they are available in environment PATH, then do:

```bash
$ pip install forth_kernel
$ python -m forth_kernel.self_install --user
```

**Note:** Currently supported on Linux only because on Windows, `gforth` doesn't work.

## Usage

- Run `jupyter notebook` (or `jupyter lab`, whichever you prefer).
- In a new or existing notebook, use the kernel selector (located at the top right of the notebook) to select `IForth`.
