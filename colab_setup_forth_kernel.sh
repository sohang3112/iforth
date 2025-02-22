#!/bin/bash

# Remove existing Jupyter kernels
rm -rf /root/.local/share/jupyter/kernels

apt install gforth 

if [ ! -d iforth ] ; then
    git clone https://github.com/sohang3112/iforth.git
fi

cd iforth

# ERROR (sometimes):
# Building wheels for collected packages: forth_kernel
#   error: subprocess-exited-with-error
  
#   × python setup.py bdist_wheel did not run successfully.
#   │ exit code: 1
#   ╰─> See above for output.
  
#   note: This error originates from a subprocess, and is likely not a problem with pip.
#   Building wheel for forth_kernel (setup.py) ... error
#   ERROR: Failed building wheel for forth_kernel
#   Running setup.py clean for forth_kernel
# Failed to build forth_kernel
# ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (forth_kernel)

pip install .
#pip install forth_kernel      # WORKING, although it seems not to have installed kernelspec

jupyter kernelspec install --user ./forth/

# IPC Proxy shouldn't be required for our jupyter kernel impl in pure Python; below was from a Rust kernel

# # Download and install IPC Proxy
# wget -qO- https://gist.github.com/wiseaidev/bc102165f43db4ebd84fcdb4c5bfb129/archive/b087c21310402bc999b36fecaf63207c74cf5b90.tar.gz | tar xvz --strip-components=1
# python install_ipc_proxy_kernel.py --quiet --kernel=forth --implementation=ipc_proxy_kernel.py > /dev/null

# # Update kernel display name
# sed -i 's/"display_name": "IForth"/"display_name": "IForth-TCP"/g' /root/.local/share/jupyter/kernels/forth_tcp/kernel.json

# WORKS TILL ABOVE - ERROR IN BELOW LINE: (no error message shown, jupyter notebook simply crashes and has to be restarted in Google Colab)
# Restart Jupyter notebook
bash -c "killall jupyter-notebook ; sleep 3 ; jupyter notebook --ip=172.28.0.12 --port=9000" </dev/null>/dev/null &
