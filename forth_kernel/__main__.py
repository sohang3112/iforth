from ipykernel.kernelapp import IPKernelApp
import shutil 

from .forth_kernel import ForthKernel

assert shutil.which('gforth') is not None, 'Program gforth not found. Please install it and ensure it is on your Environment PATH.'
IPKernelApp.launch_instance(kernel_class=ForthKernel)
