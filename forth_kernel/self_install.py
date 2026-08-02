"""Install Forth kernel by registering it with Jupyter."""
import logging
import json
import sys
from argparse import ArgumentParser
from pathlib import Path

from ipykernel.kernelapp import IPKernelApp
from jupyter_client.kernelspec import install_kernel_spec

logger = logging.getLogger('forth_kernel')
logger.setLevel(logging.INFO)
logger.info('Installing Forth kernel...')

parser = ArgumentParser()
parser.add_argument('--user', action='store_true', help='Install this Jupyter Kernel for the current user only.')
args = parser.parse_args()

# dynamically generate kernel.json so that correct Python path is used
kernel_spec = {
    "argv": [
        # path to python (of the venv where forth_kernel is installed) - allows it to run even if Jupyter is installed in a different venv
        sys.executable,
        "-m",
        "forth_kernel",
        "-f",
        "{connection_file}"
    ],
    "display_name": "IForth",
    "language": "Forth",
    "codemirror_mode": "text",
    "interrupt_mode": "message",
    "name": "Forth"
}

script_dir = Path(__file__).parent.resolve()
logger.info('Script Dir: %s', script_dir)
with (script_dir / 'kernel.json').open('w') as f:
    json.dump(kernel_spec, f, indent=4)

try:
    install_kernel_spec(str(script_dir), 'forth', replace=True, user=args.user)
    logger.info('Successfully installed jupyter kernel for Forth.')
except PermissionError as e:
    logger.error('Failed to install jupyter kernel for Forth: %s\nTry installing as user instead of root: python -m forth_kernel.self_install --user', e)
except Exception as e:
    logger.error('Failed to install jupyter kernel for Forth: %s', e)