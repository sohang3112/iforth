import asyncio
import atexit
import importlib_metadata
import logging
import os
import shutil
import signal
import sys
from pathlib import Path
from typing import Any, Callable, Literal, override

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

async def read_chunks(file, chunk_size: int, timeout: int):
    while True:
        try:
            chunk = await asyncio.wait_for(file.read(chunk_size), timeout=timeout)
            if not chunk:
                break
            yield chunk
        except asyncio.TimeoutError:
            break

async def skip_output_text(file, text: str) -> None:
    """Skip specific output text from file handle."""
    chunk = await file.read(len(text))
    if chunk.decode() != text:
        raise ValueError(f"Expected text: {text}, got: {chunk.decode()}")

class GForth:
    """Run Forth code using GForth.

    >>> async def test():
    ...     async with GForth() as gforth:
    ...         ans = await gforth.exec('3 0 1 2 + .', print_func=lambda text, stream: None)       # suppress output
    ...     print(ans.rstrip())
    >>> asyncio.get_event_loop().run_until_complete(test())
    .s <2> 3 0  ok
    """
    executable_path = gforth_path()
    output_timeout = 2     # seconds
    chunk_size = 64        # max output characters to print in one go

    def __init__(self):
        self._process = None

    def initialized(self) -> bool:
        return self._process is not None
    
    async def start(self) -> None:
        """Start GForth process."""
        if self._process is None:
            self._process = await asyncio.create_subprocess_exec(
                self.executable_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            atexit.register(self._process.terminate)
            self.banner = ''.join([chunk.decode() async for chunk in read_chunks(self._process.stdout, self.chunk_size, timeout=self.output_timeout)])
            self.version = self.banner.partition(",")[0]
            logger.info("GForth version: %s", self.version)

    def terminate(self) -> int | None:
        """Terminate GForth process.
        
        @return: Exit code of the process.
        """
        if self._process is None:
            return None
        self._process.terminate()
        exit_code = self._process.poll()
        self._process = None
        return exit_code

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        self.terminate()

    async def _exec_code_line(self, cmd: str, print_func: Callable[[str, Literal['stdout', 'stderr']], None]) -> bool:
        """Execute a single line of Forth code.

        @param cmd: Forth code to execute.
        @param print_func: Function to print output. It recieves argument for whether stdout or stderr is to be used.
        @return: Whether the execution was successful (i.e. no error occurred).
        """
        successful = True
        self._process.stdin.write(cmd.encode() + b'\n')
        await skip_output_text(self._process.stdout, cmd)        # GForth echoes the command, skip it
        async for chunk in read_chunks(self._process.stdout, self.chunk_size, timeout=self.output_timeout):
            print_func(chunk.decode(), 'stdout')
        async for chunk in read_chunks(self._process.stderr, self.chunk_size, timeout=self.output_timeout):
            successful = False
            print_func(chunk.decode(), 'stderr')
        return successful

    async def exec(self, code: str, print_func: Callable[[str, Literal['stdout', 'stderr']], None] = print_terminal) -> str | None:
        """Execute Forth code.

        @param code: Forth code to execute.
        @param print_func: Function to print output. It recieves argument for whether stdout or stderr is to be used.
        """
        if self._process is None:
            raise ValueError("GForth process not started - first call .start() method.")

        logger.info("Executing Forth code: %s", code)
        for cmd_bytes in code.encode().splitlines():
            successful = await self._exec_code_line(cmd_bytes.decode(), print_func)
            exit_code = self._process.poll()
            if exit_code is not None:
                print_func(f"GForth process exited with code {exit_code}.", 'stderr')
                sys.exit(exit_code)
            if not successful:
                return None
        
        # get Forth stack contents
        stack_output = ''
        def print_stack(text: str, stream: Literal['stdout', 'stderr']):
            if stream == 'stdout':
                nonlocal stack_output
                stack_output += text
            else:    
                print_func(text, 'stderr')

        successful = await self._exec_code_line('.s', print_stack)
        return stack_output if successful and stack_output else None
        
    async def interrupt(self) -> str:
        """Sends Ctrl+C to GForth process, and returns its error message."""
        self._process.send_signal(signal.SIGINT)
        return ''.join([chunk.decode() async for chunk in read_chunks(self._process.stderr, self.chunk_size, timeout=self.output_timeout)])

#class IForth(IPythonKernel):  
class IForth(Kernel):
    """Jupyter kernel for Forth language."""
    implementation = "forth"
    implementation_version = __version__

    gforth = GForth()
    
    def answer_text(self, text: str, stream: Literal["stdout", "stderr"]) -> None:
        """Send text response to Jupyter cell."""
        logger.info("Answering to Jupyter: %s", text)
        self.send_response(
            self.iopub_socket, "stream", {"name": stream, "text": text + "\n"}
        )

    def answer_expression_value(self, expression_value: str) -> None:
        self.send_response(self.iopub_socket, "execute_result", {
            "execution_count": self.execution_count,
            "data": {
                "text/plain": expression_value,
            },
            "metadata": {}
        })

    @override
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
        stack_output = await self.gforth.exec(code, self.answer_text)    # of the form: <2> 1 2  ok  (we should parse, <0> means no stack, so shouldn't respond)
        if stack_output is not None:
            self.answer_expression_value(stack_output)
        return {
            'status': 'ok', 
            'execution_count': self.execution_count, 
            'payload': [], 
            'user_expressions': {}
        }

    # BUG: doesnt seem to be called (the log message is not printed in `tail -F ~/.jupyter/forth_kernel.log`)
    @override
    def do_shutdown(self, restart: bool) -> dict[str, str | bool]:
        """Shutdown the kernel."""
        logger.info("do_shutdown (restart=%s)", restart)
        self.gforth.terminate()
        return {'status': 'ok', 'restart': restart}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
