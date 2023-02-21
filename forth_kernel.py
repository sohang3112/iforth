from ipykernel.kernelbase import Kernel

from typing import Any, Dict, Literal
from subprocess import check_output, PIPE, Popen
from threading import Thread
from functools import cached_property
import re
import os
import sys
import time

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

__version__ = '0.2'
__path__ = os.environ.get('GFORTHPATH')

class ForthKernel(Kernel):
    implementation = 'forth_kernel'
    implementation_version = __version__
    language = 'forth'
    first_command = True

    @property
    def language_version(self) -> str:
        return self.banner.split(' ')[-1]

    @cached_property
    def banner(self) -> str:
        return check_output(['gforth', '--version']).decode('utf-8')

    language_info = {
        'name': 'forth_kernel',
        'version': '0.2',
        'mimetype': 'text',
        'file_extension': '.4th'
	}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()
        
        self._gforth = Popen('gforth', stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=2, close_fds=ON_POSIX)
        self._gforth_stdout_queue = Queue()
        self._gforth_stderr_queue = Queue()

        t_stdout = Thread(target=enqueue_output, args=(self._gforth.stdout, self._gforth_stdout_queue))
        t_stdout.daemon = True
        t_stdout.start()

        t_stderr = Thread(target=enqueue_output, args=(self._gforth.stderr, self._gforth_stderr_queue))
        t_stderr.daemon = True
        t_stderr.start()    


    def answer(self, output: str, stream_name: str):
        """@param stream_name: 'stdout' | 'stderr'"""
        stream_content = {'name': stream_name, 'text': output}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def get_queue(self, queue: Queue) -> str:
        output = ''
        line = b'.'
        timeout = 3.
        while len(line) or timeout > 0.:
            try:
                line = queue.get_nowait()
            except Empty:
                line = b''
                if timeout > 0.:
                    time.sleep(0.01)
                    timeout -= 0.01
            else:
                try:
                    output += line.decode()
                except UnicodeDecodeError:
                    output += line.decode('latin-1')
                timeout = 0.
        return output


    def do_execute(self, code: str, silent: bool, store_history=True, user_expressions=None, allow_stdin=False) -> Dict[str, Any]:
        if self._gforth_stdout_queue.qsize():
            output = self.get_queue(self._gforth_stdout_queue)
        if self._gforth_stderr_queue.qsize():
            error = self.get_queue(self._gforth_stderr_queue)
        
        self._gforth.stdin.write((code + '\n').encode('utf-8'))
        output = self.get_queue(self._gforth_stdout_queue)
        error = self.get_queue(self._gforth_stderr_queue)

        # Return results.
        if not silent:
            self.answer(output + '\n', 'stdout')
            if error:
                self.answer(error + '\n', 'stderr')       

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}
    
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    import shutil 

    assert shutil.which('gforth') is not None, 'Program gforth not found. Please install it and ensure it is on your Environment PATH.'
    IPKernelApp.launch_instance(kernel_class=ForthKernel)
