import html
import os
import re
import sys
import time
from difflib import SequenceMatcher
from functools import cached_property
from subprocess import PIPE, Popen, check_output
from threading import Thread
from typing import Any, Dict, Literal

from ipykernel.kernelbase import Kernel

try:
    from Queue import Empty, Queue
except ImportError:
    from queue import Empty, Queue  # python 3.x

__version__ = '0.2'
__path__ = os.environ.get('GFORTHPATH')


class ForthKernel(Kernel):
    implementation = 'forth_kernel'
    implementation_version = __version__
    language = 'forth'
    first_command = True

    @property
    def language_version(self) -> str:
        return self.banner.partition(',')[0]

    language_info = {
        'name': 'forth',
        'version': '0.3',
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

        self.banner = self.get_queue(self._gforth_stdout_queue)

    def get_queue(self, queue: Queue) -> str:
        output = ''
        line = b'.'
        timeout = 5.
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

    def answer_text(self, text: str, stream: Literal['stdout', 'stderr']):
        self.send_response(self.iopub_socket, 'stream', {
            'name': stream, 
            'text': text + '\n'
        }) 

    def answer_html(self, html: str):
        self.send_response(self.iopub_socket, 'display_data', {
            'metadata': {},
            'data': {
                'text/html': html
            }
        })

    def success_response(self):
        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}

    # TODO: Arguments (store_history, user_expressions, allow_stdin) are unused <- use them!
    # BUG: (maybe!) a long-running continous shell output may not show in Jupyter cell output
    #   Eg. an infinite loop printing same line continously
    #   FIX: show code output line by line instead of all at once
    def do_execute(self, code: str, silent: bool, store_history=True, user_expressions=None, allow_stdin=False) -> Dict[str, Any]:
        if code.startswith('!'):                # Shell Command
            self.answer_text(check_output(code[1:], encoding='utf-8'), 'stdout')
            return self.success_response()

        self._gforth.stdin.write((code + '\n').encode('utf-8'))

        output = self.get_queue(self._gforth_stdout_queue)
        error = self.get_queue(self._gforth_stderr_queue)

        # Return Jupyter cell output.
        if not silent:
            code, output = html.escape(code), html.escape(output)
            s = SequenceMatcher(lambda x: x == '', code, output)
            # TODO: refactor
            html_output = '<pre>' + ''.join(
                '<b>' + output[j1:j2] + '</b>' if tag in ('insert', 'replace') else output[j1:j2]
                for tag, i1, i2, j1, j2 in s.get_opcodes()
            ) + '</pre>'
            self.answer_html(html_output)

            if error:
                self.answer_text(error, 'stderr')  

        exit_code = self._gforth.poll()
        if exit_code is not None:
            self.answer('Killing kernel because GForth process has died\n', 'stderr')
            sys.exit(exit_code)     

        return self.success_response()