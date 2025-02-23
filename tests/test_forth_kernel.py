import unittest
import jupyter_kernel_test


class MyKernelTests(jupyter_kernel_test.KernelTests):
    kernel_name = "forth"
    language_name = "forth"

    # code_hello_world = '." Hello, world!" cr'
    code_execute_result = [{"code": '." Hello World" cr', "result": "Hello World\n"}]
    # AssertionError: execute_result message not found


if __name__ == "__main__":
    unittest.main()

# from pathlib import Path

# from nbclient import NotebookClient
# import nbformat

# script_dir = Path(__file__).parent
# nb = nbformat.read(script_dir / 'demo_forth_notebook.ipynb', as_version=4)
# client = NotebookClient(nb, kernel_name='forth')
# x = client.execute()
# print(x)
# # {'cells': [{'cell_type': 'code',
# #             'execution_count': 1,
# #             'metadata': {'execution': {'iopub.execute_input': '2025-02-23T06:45:53.319440Z',
# #                                        'iopub.status.busy': '2025-02-23T06:45:53.314886Z',
# #                                        'iopub.status.idle': '2025-02-23T06:45:58.426794Z',
# #                                        'shell.execute_reply': '2025-02-23T06:45:58.426117Z'}},
# #             'outputs': [{'data': {'text/html': '<pre>1 2 + .<b> 3  ok\n'
# #                                                '</b></pre>'},
# #                          'metadata': {},
# #                          'output_type': 'display_data'}],
# #             'source': '1 2 + .'}],
# #  'metadata': {'language_info': {'file_extension': '.4th',
# #                                 'mimetype': 'text',
# #                                 'name': 'forth',
# #                                 'version': '0.4.1'}},
# #  'nbformat': 4,
# #  'nbformat_minor': 2}