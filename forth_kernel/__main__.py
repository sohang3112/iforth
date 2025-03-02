import asyncio

import nest_asyncio
from ipykernel.kernelapp import IPKernelApp

from . import IForth

# Allows asyncio.run() to be called multiple times.
# Source: https://stackoverflow.com/a/56434301/12947681
nest_asyncio.apply()

async def main():
    await IForth.gforth.start()         # TODO: instead use async with for GForth()
    IForth.banner = IForth.gforth.banner
    IForth.language_info = {
        "name": "forth",
        "version": IForth.gforth.version,
        "mimetype": "text",
        "file_extension": ".4th",
    }
    IPKernelApp.launch_instance(kernel_class=IForth)

asyncio.run(main())


