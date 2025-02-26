import asyncio

import nest_asyncio
from ipykernel.kernelapp import IPKernelApp

from . import IForth

nest_asyncio.apply()

async def main():
    await IForth.gforth.start()
    IForth.banner = IForth.gforth.banner
    IForth.language_info = {
        "name": "forth",
        "version": IForth.gforth.version,
        "mimetype": "text",
        "file_extension": ".4th",
    }
    IPKernelApp.launch_instance(kernel_class=IForth)

asyncio.get_event_loop().run_until_complete(main())


