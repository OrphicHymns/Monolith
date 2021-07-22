import os
import ctypes
import logging
from time import strftime
from uuid import uuid4
from typing import Optional, Union

import toml
import asyncio
from aiofiles import open
from easygui import fileopenbox
from aiohttp_proxy import ProxyConnector, ProxyType

from checker.types import File
from checker.color import Color
from checker.constants import CONFIG


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def set_title(title: str) -> None:
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def create_mojang_payload(email: str, password: str) -> dict:
    return {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": email,
        "password": password,
        "clientToken": str(uuid4()),
        "requestUser": True
    }


async def error(message: str) -> None:
    print(f"{Color.WHITE}[{Color.RED}ERROR{Color.WHITE}] {message}")

    for i in range(5):
        print(f"{Color.WHITE}[{Color.RED}ERROR{Color.WHITE}] This program will continue in {5 - i} seconds.", end="\r")
        await asyncio.sleep(1)

    clear()


async def create_config() -> None:
    await (await open("config.toml", "w", encoding="utf-8")).write(CONFIG)


async def parse_config() -> dict:
    try:
        return toml.loads(await (await open("config.toml", "r", encoding="utf-8")).read())
    except FileNotFoundError:
        await error("Config file not found, creating new config and using the default one.")
        await create_config()
        return toml.loads(CONFIG)
    except toml.TomlDecodeError:
        await error("Failed to parse config, using default config.")
        return toml.loads(CONFIG)


async def load_file(file: File) -> Optional[set[str]]:
    while True:
        try:
            if os.name == "nt":
                file_name = fileopenbox(title=f"Load {file}")
            else:
                file_name = input(f"{file}: ")

            lines = set((await (await open(file_name, "r", encoding="utf-8", errors="ignore")).read()).splitlines())

            if lines.__contains__(""):
                lines.remove("")

            return lines
        except Exception:
            pass


async def get_input(
        message: Optional[str] = None, choices: Optional[tuple[str, ...]] = None, convert_int: Optional[bool] = False
) -> Union[str, int]:
    while True:
        if message is not None:
            logging.info(message)

        inp = input(" > ")

        if choices is not None:
            if choices.__contains__(inp.lower()):
                return inp
        elif convert_int is True:
            try:
                return int(inp)
            except Exception:
                pass
        elif inp not in ("", " "):
            return inp


def parse_proxy(proxy: str, proxy_type: str) -> Optional[ProxyConnector]:
    if proxy_type == "http":
        proxy_type = ProxyType.HTTP
    elif proxy_type == "https":
        proxy_type = ProxyType.HTTPS
    elif proxy_type == "socks4":
        proxy_type = ProxyType.SOCKS4
    else:
        proxy_type = ProxyType.SOCKS5

    spl = proxy.split(":")

    if proxy.count(":") == 3:
        return ProxyConnector(
            proxy_type=proxy_type,
            host=spl[0],
            port=spl[1],
            username=spl[2],
            password=spl[3]
        )
    else:
        return ProxyConnector(
            proxy_type=proxy_type,
            host=spl[0],
            port=int(spl[1])
        )


def create_results():
    time = str(strftime('Monolith-%d-%m-%Y %H-%M-%S'))
    results = f"results/{time}"
    if not os.path.exists('results'):
        os.mkdir('results')
    if not os.path.exists(results):
        os.mkdir(results)
    return results
