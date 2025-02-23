import logging
import shutil
import sys
from argparse import ArgumentParser
from pathlib import Path

from ipykernel.kernelapp import IPKernelApp
from jupyter_client.kernelspec import install_kernel_spec

from .forth_kernel import ForthKernel

IPKernelApp.launch_instance(kernel_class=ForthKernel)
#app = IPKernelApp.instance(kernel_class=ForthKernel)
#app.initialize()
#app.start()


