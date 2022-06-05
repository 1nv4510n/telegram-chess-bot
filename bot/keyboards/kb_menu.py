from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def make_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text='New game'), KeyboardButton(text='Help'))
    keyboard.row(KeyboardButton(text='Statistics'))
    
    return keyboard.as_markup(resize_keyboard=True)