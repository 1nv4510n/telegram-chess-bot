from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.chess.enums import PieceIcons

def make_pieces_keyboard(pieces: List[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    
    for piece in pieces:
        keyboard.add(KeyboardButton(text=piece.value))
        
    keyboard.row(KeyboardButton(text='Resign'))
    
    return keyboard.as_markup(resize_keyboard=True)