"""Test the Forth jupyter kernel.

Run tests:
$ uv run --group test python tests/test_forth_kernel.py
"""
import jupyter_kernel_test


class MyKernelTests(jupyter_kernel_test.KernelTests):
    kernel_name = "forth"
    language_name = "forth"
    file_extension = ".4th"

    code_hello_world = '." hello, world"'
    code_stderr = 'clearstack .'      # stack underflow error
    code_execute_result = [
        {'code': '1 2 3 .', 'result': '.s <2> 1 2  ok\n'},
    ]
    

if __name__ == "__main__":
    import unittest
    unittest.main()