import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from magic_filter import F
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import config
from .commands import set_commands

from .db.base import Base
from .middlewares.db_middleware import DbSessionMiddleware

from .handlers.users import default


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    engine = create_async_engine(config.postgres_dsn, future=True, echo=False)

    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))
        
    dp.message.filter(F.chat.type == 'private')
    
    dp.message.middleware(DbSessionMiddleware(db_pool))
    
    dp.include_router(default.router)
    
    await set_commands(bot)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()