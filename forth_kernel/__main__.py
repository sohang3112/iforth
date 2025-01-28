import logging
import shutil
import sys
from argparse import ArgumentParser
from pathlib import Path

from ipykernel.kernelapp import IPKernelApp
from jupyter_client.kernelspec import install_kernel_spec

from .forth_kernel import ForthKernel

logger = logging.getLogger('forth_kernel')
logger.setLevel(logging.INFO)

if shutil.which('gforth') is None:
    logger.error('Program gforth not found. Please install it and ensure it is on your Environment PATH.')
    sys.exit(1)

parser = ArgumentParser()
parser.add_argument('--install', action='store_true', help='Install this Jupyter Kernel to add support for the Forth programming language.')
args = parser.parse_args()
logger.info('--installed=%s', args.install)

# if args.install:
#     script_dir = Path(__file__).parent.resolve()
#     logger.info('Script Dir: %s', script_dir)
#     install_kernel_spec(str(script_dir), 'forth', replace=True)
# else:       # Launch the kernel
#     IPKernelApp.launch_instance(kernel_class=ForthKernel)
app = IPKernelApp.instance()


