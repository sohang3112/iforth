"""Install Forth kernel by registering it with Jupyter."""
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
logger.info('Installing Forth kernel...')

parser = ArgumentParser()
parser.add_argument('--user', action='store_true', help='Install this Jupyter Kernel for the current user only.')
args = parser.parse_args()

script_dir = Path(__file__).parent.resolve()
logger.info('Script Dir: %s', script_dir)
try:
    install_kernel_spec(str(script_dir), 'forth', replace=True, user=args.user)
    logger.info('Successfully installed jupyter kernel for Forth.')
except PermissionError as e:
    logger.error('Failed to install jupyter kernel for Forth: %s\nTry installing as user instead of root: python -m forth_kernel.self_install --user', e)
except Exception as e:
    logger.error('Failed to install jupyter kernel for Forth: %s', e)