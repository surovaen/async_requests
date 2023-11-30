import asyncio

from worker import Worker


class Client:
    """Класс Клиент, запускает и останавливает работу воркера."""

    def __init__(self):
        """Инициализация параметров."""
        self.queue = asyncio.Queue()
        self.worker = Worker(queue=self.queue)

    def create_requests(self, request_id: int):
        """Метод отправки сообщений в очередь."""
        self.queue.put_nowait(request_id)

    async def start(self):
        """Метод запуска работы клиента."""
        await self.worker.start()

    async def stop(self):
        """Метод завершения работы клиента."""
        await self.worker.stop()
