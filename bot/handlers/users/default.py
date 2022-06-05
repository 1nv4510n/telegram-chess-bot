from uuid import uuid4
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(commands=['start'])
async def command_start(message: Message):
    await message.answer('Hello!')