import asyncio
from asyncio import Queue
import json

import aiohttp
from loguru import logger
from tqdm import tqdm

from config import Config as settings


class Worker:
    """Класс Воркер, осуществляет выполнение задач."""

    WORKERS = settings.WORKERS

    def __init__(self, queue: Queue):
        """Инициализация параметров."""
        self.queue = queue
        self._tasks = []
        self._responses = []
        self.bar = tqdm(
            desc='Выполнение',
            total=settings.REQUESTS_COUNT,
            ncols=100,
            colour='#C0C0C0',
        )

    async def _worker(self):
        """Метод получения новых сообщений и их обработки."""
        while True:
            request_id = await self.queue.get()

            try:
                request_url = settings.FAKE_API + str(request_id)
                response = await self._request(request_url)
                self._responses.append(response)

            except Exception as e:
                logger.error('Ошибка выполнения запроса: {exc}'.format(exc=e))

            finally:
                self.queue.task_done()
                self.bar.update(1)

    def _write_json(self):
        """Метод записи полученных респонсов в result.json."""
        with open(settings.RESULT_JSON, 'w') as file:
            json.dump(
                self._responses,
                file,
                indent=4,
                separators=(',', ': '),
            )

    async def _request(self, request_url: str):
        """Метод запроса на фейковый API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                return await response.json()

    async def start(self):
        """Метод запуска воркера."""
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.WORKERS)]

    async def stop(self):
        """Метод остановки воркера."""
        await self.queue.join()
        self._write_json()
        for task in self._tasks:
            task.cancel()
