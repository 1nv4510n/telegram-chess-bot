import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.telegram import TelegramAPIServer
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram import F

from aiohttp import web

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import config
from .commands import set_commands

from .db.requests import reset_users_table
from .middlewares import DbSessionMiddleware
from .utils import log

from . import handlers

async def main():
    engine = create_async_engine(config.postgres_dsn, future=True, echo=False)

    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(config.custom_bot_api, is_local=True)
    
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))

    dp.message.filter(F.chat.type == "private")
    
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    dp.include_router(handlers.router)

    await set_commands(bot)
    
    try:
        if not config.webhook_domain:
            log.info('BOT STARTED!')
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )

            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()
            log.info('BOT STARTED')
            
            await asyncio.Event().wait()
    finally:
        await reset_users_table(db_pool)
        log.info('BOT STOPPED')
        await bot.session.close()