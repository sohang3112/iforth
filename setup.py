""" Setup script for forth_kernel package. """

import os
import shutil
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install


def install_with_kernelspec(*args):
    from jupyter_client.kernelspec import install_kernel_spec
    print('install_with_kernelspec arguments:', args)
    project_dir = os.path.dirname(os.path.realpath(__file__))
    print('Project Dir:', project_dir)
    install_kernel_spec(os.path.join(project_dir, 'kernelspec'), 'forth', replace=True)

class CustomInstallCommand(install):
    def run(self):
        print('in CustomInstallCommand.run()')
        install.run(self)
        install_with_kernelspec()

class CustomDevelopCommand(develop):
    def run(self):
        print('in CustomDevelopCommand.run()')
        develop.run(self)
        install_with_kernelspec()

class CustomEggInfoCommand(egg_info):
    def run(self):
        print('in CustomEggInfoCommand.run()')
        egg_info.run(self)
        install_with_kernelspec()

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

packages_required = ['pexpect>=3.3', 'jupyter_client', 'ipykernel']

setup(name='forth_kernel',
      version='0.3',
      description='Jupyter kernel for Forth language (Fork of https://github.com/jdfreder/iforth)',
      long_description=readme,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      include_package_data=True,
      author='Sohang Chopra',
      author_email='sohangchopra@gmail.com',
      url='https://github.com/sohang3112/iforth',
      py_modules=['forth_kernel'],
      cmdclass={'install': CustomInstallCommand},
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
