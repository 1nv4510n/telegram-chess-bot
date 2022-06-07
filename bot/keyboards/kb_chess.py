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

def make_select_keyboard(select_pieces: List[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    
    for piece in select_pieces:
        keyboard.add(KeyboardButton(text=piece))
        
    keyboard.row(KeyboardButton(text='Change piece'))
    
    return keyboard.as_markup(resize_keyboard=True)

def make_target_keyboard(targets: List[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    
    for target in targets:
        keyboard.add(KeyboardButton(text=target))
        
    keyboard.row(KeyboardButton(text='Change piece'))
    
    return keyboard.as_markup(resize_keyboard=True)