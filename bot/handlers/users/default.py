from aiogram import Router, F
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.search_filter import UserSearchingFilter

from bot.keyboards.kb_default import make_menu_keyboard
from bot.db.requests import add_user
from bot.states import ChessStates

router = Router()

@router.message(UserSearchingFilter(searching=False), commands=['start'])
async def command_start(message: Message, session: AsyncSession):
    await add_user(session, message.chat.id)
    await message.answer("Let's play chess!", reply_markup=make_menu_keyboard())

@router.message(commands=['help'])
@router.message(F.text.lower() == 'help')
async def command_help(message: Message):
    await message.answer(
        f'How to play chess: \nhttps://www.instructables.com/Playing-Chess/', 
        reply_markup=make_menu_keyboard()
        )