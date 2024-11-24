# TODO: Do pip install and run jupyter as non-root user

ARG version=stable

FROM jupyter/base-notebook AS base
MAINTAINER Sohang Chopra <sohangchopra@gmail.com>
LABEL maintainer="Sohang Chopra <sohangchopra@gmail.com>"
LABEL description="Jupyter Notebook with Forth Kernel"

USER root
RUN chown jovyan /home/jovyan
RUN apt-get -y update &&\ 
    DEBIAN_FRONTEND=noninteractive apt-get -qq install gforth

USER jovyan
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

FROM base AS stable
RUN pip install forth_kernel
RUN python -c 'import importlib.resources as r; print(r.files("forth_kernel"))'
RUN jupyter kernelspec install --user $(python -c 'import importlib.resources as r; print(r.files("forth_kernel"))')/forth

FROM base AS development
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install git
RUN pip install git+https://github.com/sohang3112/iforth.git
ARG temp=dummy
RUN python -c 'import importlib.resources as r; print(r.files("forth_kernel"))'
RUN jupyter kernelspec install --user $(python -c 'import importlib.resources as r; print(r.files("forth_kernel"))')/forth

FROM base AS testing
WORKDIR /home/jovyan/.local
COPY README.md .
COPY setup.py .
COPY forth_kernel forth_kernel/
COPY forth/ forth/
RUN pip install -e . --verbose
RUN jupyter kernelspec install --user forth      

FROM ${version} AS final
WORKDIR /home/jovyan
EXPOSE 8888
CMD jupyter kernelspec list && jupyter notebook --allow-root --NotebookApp.kernel=forth_kernel 