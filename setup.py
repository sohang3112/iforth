from setuptools import setup
from setuptools.command.install import install
import sys
import os
import shutil

class install_with_kernelspec(install):
    def run(self):
        install.run(self)
        from jupyter_client.kernelspec import install_kernel_spec
        project_dir = os.path.dirname(os.path.realpath(__file__))
        install_kernel_spec(os.path.join(project_dir, 'kernelspec'), 'forth', replace=True)

with open('README.md') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

packages_required = ['pexpect>=3.3', 'jupyter_client', 'ipykernel']

setup(name='forth_kernel',
      version='0.3',
      description='A Forth kernel for IPython (Fork of https://github.com/jdfreder/iforth)',
      long_description=readme,
      long_description_content_type='text/markdown',
      include_package_data=True,
      author='Sohang Chopra',
      author_email='sohangchopra@gmail.com',
      url='https://github.com/sohang3112/iforth',
      py_modules=['forth_kernel'],
      cmdclass={'install': install_with_kernelspec},
      setup_requires=packages_required,
      install_requires=packages_required,
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ]
)

if shutil.which('gforth') is None:
    print('WARNING: gforth not found on Environment PATH. Please install gforth.')
