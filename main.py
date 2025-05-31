import asyncio
import logging

from database import db_manager
from tg_bot import start_bot


async def main():
    db_manager.start_app()

    await start_bot()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
