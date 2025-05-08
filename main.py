import asyncio
import logging



async def main():
    await start_bot()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
