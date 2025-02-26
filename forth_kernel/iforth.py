import asyncio
import atexit
import importlib_metadata
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Callable, Literal

from ipykernel.kernelbase import Kernel
from ipykernel.ipkernel import IPythonKernel

__version__ = importlib_metadata.version("forth_kernel")

logger = logging.getLogger('forth_kernel')
logger.setLevel(logging.INFO)
log_file_path = Path.home() / '.jupyter' / 'forth_kernel.log'
logger.addHandler(logging.FileHandler(log_file_path))

def gforth_path() -> str:
    ans = os.environ.get("GFORTHPATH") or shutil.which('gforth')
    if ans is None:
        raise FileNotFoundError("GForth executable not found.")
    return ans

def print_terminal(text: str, stream: Literal['stdout', 'stderr']) -> None:
    """Print text to terminal."""
    getattr(sys, stream).write(text)

async def read_lines(file, timeout: int):
    while True:
        try:
            line = await asyncio.wait_for(file.readline(), timeout=timeout)
            if not line:
                break
            yield line
        except asyncio.TimeoutError:
            break

class GForth:
    """Run Forth code using GForth.

    >>> async def test():
    ...     async with GForth() as gforth:
    ...         await gforth.exec('1 2 + .')
    ...     print(gforth.version())
    >>> asyncio.get_event_loop().run_until_complete(test())
    1 2 + . 3  ok
    Gforth 0.7.3
    """
    executable_path = gforth_path()
    line_timeout = 2     # seconds

    def __init__(self):
        self._process = None

    def initialized(self) -> bool:
        return self._process is not None
    
    async def start(self) -> None:
        """Start GForth process."""
        self._process = await asyncio.create_subprocess_exec(
            self.executable_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        atexit.register(self._process.terminate)
        self.banner = ''.join([line.decode() async for line in read_lines(self._process.stdout, timeout=self.line_timeout)])
        self.version = self.banner.partition(",")[0]
        logger.info("GForth version: %s", self.version)

    async def __aenter__(self):
        self.start()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        self._process.terminate()

    async def exec(self, code: str, print_func: Callable[[str, Literal['stdout', 'stderr']], None] = print_terminal) -> None:
        """Execute Forth code.
        @param code: Forth code to execute.
        @param print_func: Function to print output. It recieves argument for whether stdout or stderr is to be used.
        """
        logger.info("Executing Forth code: %s", code)
        error_occurred = False
        for cmd_bytes in code.encode().splitlines():
            self._process.stdin.write(cmd_bytes + b'\n')
            async for line in read_lines(self._process.stdout, timeout=self.line_timeout):
                print_func(line.decode(), 'stdout')
            async for line in read_lines(self._process.stderr, timeout=self.line_timeout):
                error_occurred = True
                print_func(line.decode(), 'stderr')
            if error_occurred:
                break
            

#class IForth(IPythonKernel):  
class IForth(Kernel):
    """Jupyter kernel for Forth language."""
    implementation = "forth"
    implementation_version = __version__

    gforth = GForth()
    
    def answer_text(self, text: str, stream: Literal["stdout", "stderr"]):
        """Send text response to Jupyter cell."""
        logger.info("Answering to Jupyter: %s", text)
        self.send_response(
            self.iopub_socket, "stream", {"name": stream, "text": text + "\n"}
        )

    async def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions = None,
        allow_stdin = None,
        *,
        cell_meta = None,
        cell_id = None,
    ) -> dict[str, Any]:
        """Execute Forth code."""
        logger.info("do_execute (silent=%s): %s", silent, code)
        if not silent:
            await self.gforth.exec(code, self.answer_text)
        return {
            'status': 'ok', 
            'execution_count': self.execution_count, 
            'payload': [], 
            'user_expressions': {}
        }

if __name__ == '__main__':
    import doctest
    doctest.testmod()
