import threading

import asyncio


class Worker(threading.Thread):
    def __init__(self, queue: asyncio.Queue, workers: int):
        super().__init__()
        self.queue = queue
        self.workers = workers

    async def worker(self):
        while True:
            try:
                item = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            await item
            self.queue.task_done()

    def run(self):
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*[self.worker() for _ in range(self.workers)]))
