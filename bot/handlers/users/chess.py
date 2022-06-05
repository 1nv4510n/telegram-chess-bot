from aiogram import Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.states import ChessStates

router = Router()