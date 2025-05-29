from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Bot

BOT = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# Paths
BASE_DIR = Path(__file__).resolve().parent
WEIGHTS_PATH = (BASE_DIR / 'routers' / 'analysis_methods' / 'backend'
                / 'cnn_analysis_method' / 'cnn_weights' / 'best.pt')
PATTERNS_PATH = BASE_DIR / 'static' / 'generate_patterns'