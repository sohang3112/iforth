"""Test the Forth jupyter kernel.

Run tests:
$ uv run --group test python tests/test_forth_kernel.py
"""
import jupyter_kernel_test
import unittest
import time
from forth_kernel.iforth import strip_prompt

class StripPromptTests(unittest.TestCase):
    def test_prompt_only(self):
        self.assertEqual(strip_prompt('  ok\n'), '')

    def test_keeps_trailing_newline_of_output(self):
        self.assertEqual(strip_prompt('\n67 \n ok\n'), '\n67 \n')

    def test_compiled_prompt(self):
        self.assertEqual(strip_prompt(': foo 1 ; compiled'), ': foo 1 ;')

    def test_no_prompt_is_unchanged(self):
        self.assertEqual(strip_prompt('no prompt here'), 'no prompt here')

class MyKernelTests(jupyter_kernel_test.KernelTests):
    kernel_name = "forth"
    language_name = "forth"
    file_extension = ".4th"

    code_hello_world = '." hello, world"'
    code_stderr = 'clearstack .'      # stack underflow error
    code_execute_result = [
        {'code': '1 2 3 .', 'result': '<2> 1 2 ok'},
    ]

    def setUp(self):
        self.flush_channels()
        
    def test_multiline_cell_is_prompt(self):
        """Regression: each line used to cost a full read timeout."""
        start = time.monotonic()
        reply, _ = self.execute_helper(code='1 .\n2 .\n3 .\n4 .\n5 .')
        self.assertEqual(reply['content']['status'], 'ok')
        self.assertLess(time.monotonic() - start, 5)

    def test_long_output_not_truncated(self):
        """Regression: output was cut off when it exceeded the read timeout."""
        _, msgs = self.execute_helper(code=': countup 200 0 do i . loop ; countup')
        out = ''.join(m['content']['text'] for m in msgs
                      if m['msg_type'] == 'stream'
                      and m['content']['name'] == 'stdout')
        self.assertIn('199', out)

if __name__ == "__main__":
    import unittest
    unittest.main()