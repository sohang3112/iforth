# IForth
Forth kernel for Jupyter notebook / lab. This is a fork of [github.com/jdfreder/iforth](https://github.com/jdfreder/iforth).

![Example Notebook Screenshot](notebook_screenshot.png)

## Installation
1. Install [Gforth](https://www.gnu.org/software/gforth/).  Make sure it is accessible via the commandline/terminal (`gforth --version`).
2. Run `pip install forth_kernel`

### Development Installation
Clone this repository and do an [editable `pip` install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs) in this repository's folder:
```bash
pip install -e .
jupyter kernelspec install ./kernelspec --user   
```

**Note:** `jupyter kernelspec install` is required here, because unlike in normal install, the kernel does NOT automatically show in `jupyter kernelspec list`.

## Usage
- Run `jupyter notebook` (or `jupyter lab`, whichever you prefer).
- In a new or existing notebook, use the kernel selector (located at the top right of the notebook) to select `IForth`.
