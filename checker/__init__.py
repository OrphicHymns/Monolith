import logging

import asyncio
from console.utils import set_title

from checker.color import Color
from checker.functions import create_config, parse_config, clear


__title__ = 'Monolith'
__version__ = '0.1-beta'
__author__ = 'Geographs#7816'
__license__ = 'MIT'


clear()
set_title(f"{__title__} {__version__} by {__author__}")


asyncio.set_event_loop(asyncio.ProactorEventLoop())
loop = asyncio.get_event_loop()

config = loop.run_until_complete(parse_config())

logging.basicConfig(
    format=f"  {Color.WHITE}[{Color.SEA_GREEN}%(levelname)s{Color.WHITE}] {Color.RESET}%(message)s",
    level=logging.NOTSET
)

if config["Monolith"]["debug"] is False:
    logging.disable(logging.DEBUG)
