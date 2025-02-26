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
    code_stderr = '.'
    # code_execute_stdout = 
    # code_execute_result = [
    #     {"code": '1 2 + .', "result": "1 2 + . 3  ok"}
    # ]  
    # AssertionError: execute_result message not found

    # code_display_data = [
    #     {
    #         "code": "from IPython.display import HTML, display; display(HTML('<b>test</b>'))",
    #         "mime": "text/html",
    #     },
    #     {
    #         "code": "from IPython.display import Math, display; display(Math('\\frac{1}{2}'))",
    #         "mime": "text/latex",
    #     },
    # ]
    

if __name__ == "__main__":
    import unittest
    unittest.main()