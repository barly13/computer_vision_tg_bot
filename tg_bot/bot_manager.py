from aiogram import Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from tg_bot.settings import BOT


async def start_bot():
    router = Router()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=router)
    await BOT.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(BOT, allowed_updates=dp.resolve_used_update_types())
