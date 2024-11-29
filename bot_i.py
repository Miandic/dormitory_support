import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from asyncpg_lite import DatabaseManager

pg_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))

admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
banned = [int(banned_id) for banned_id in config('BLACKLIST').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())