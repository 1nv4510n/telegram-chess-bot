from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils import log

from bot.filters.search_filter import UserSearchingFilter, UserPlayingFilter

from bot.db.requests import add_user
from bot.keyboards.kb_default import make_menu_keyboard

router = Router()

@router.message(UserSearchingFilter(searching=False), UserPlayingFilter(playing=False), commands=['start'])
async def command_start(message: Message, session: AsyncSession):
    await add_user(session, message.from_user.id)
    await message.answer("Let's play chess!", reply_markup=make_menu_keyboard())
    log.info(f"User '{message.from_user.first_name}' started bot!")


@router.message(commands=['help'])
@router.message(F.text.lower() == 'help')
async def command_help(message: Message):
    await message.answer(
        f'How to play chess: \nhttps://www.instructables.com/Playing-Chess/', 
        reply_markup=make_menu_keyboard()
        )