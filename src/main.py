import asyncio

from client import Client
from config import Config as settings


async def main():
    client = Client()

    for i in range(1, settings.REQUESTS_COUNT + 1):
        client.create_requests(i)

    await client.start()
    await client.stop()


if __name__ == '__main__':
    asyncio.run(main())
