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

## Documentation

See detailed documentation at [this repo's wiki](https://github.com/sohang3112/iforth/wiki). **TODO:** The wiki is empty, update docs there!

## Usage

- Run `jupyter notebook` (or `jupyter lab`, whichever you prefer).
- In a new or existing notebook, use the kernel selector (located at the top right of the notebook) to select `IForth`.

## Misc Notes

### [Jupyter Kernel Architecture](https://www.datahaskell.org/blog/2025/11/25/a-tale-of-two-kernels.html#the-jupyter-kernel-architecture)

Jupyter is essentially a front-end that communicates with a computation server via a protocol (aptly called the Jupyter protocol). This computation server is called a kernel. All jupyter needs to know about a kernel is which ports to use to communicate different kinds of messages.

The Jupyter stack looks like this:

* JupyterLab / Notebook frontend (browser): Renders notebooks, lets you edit cells, handles user events.
* Jupyter server (Python): Manages files, launches kernels, proxies messages.
* Kernel (language backend): Actually executes your code.

The frontend and the kernel do not share memory. They talk over five distinct logical channels, each responsible for a specific type of message exchange:

* Shell: The main request/reply loop. The frontend sends code execution requests here.
* IOPub: A broadcast channel. The kernel publishes “side effects” here, such as stdout, stderr, and renderable data (plots, HTML).
* Stdin: Allows the kernel to request input from the user (e.g., when a script asks for a password).
* Control: A high-priority channel for system commands (like “Shutdown” or “Interrupt”) that must bypass the execution queue.
* Heartbeat: A simple ping/pong socket to ensure the kernel is still alive.

#### Jupyter Registration Spec

Jupyter discovers kernels via a JSON specification file (kernel.json). You can list these with jupyter kernelspec list.

When Jupyter starts a kernel, it generates a connection file (represented by {connection_file} in the args above). This ephemeral JSON file tells the kernel which ports to bind to for the five channels:

```json
{  
  "shell_port": 41083,  
  "iopub_port": 42347,  
  "stdin_port": 56773,  
  "control_port": 57347,  
  "hb_port": 34681,  
  "ip": "127.0.0.1",  
  "key": "aa072f60-5cac0ac2506b1a572678209a",  
  "transport": "tcp",  
  "signature_scheme": "hmac-sha256",  
  "kernel_name": "IForth"  
}
```

Some notable fields:

* Ports: One per channel (shell_port, iopub_port, etc.).
* Key + signature_scheme: Used to sign messages (HMAC) so rogue processes can’t spoof messages.
* Transport + IP: Usually TCP over localhost, but in principle could be remote.

Each of these ports is used to send different types of payloads to the kernel. So any implementation of the Jupyter protocol needs to handle these messages correctly (or at least, gracefully).

