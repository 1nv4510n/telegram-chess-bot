from aiogram.types import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def make_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text='New game'))
    keyboard.row(KeyboardButton(text='Statistics'), KeyboardButton(text='Leaderboard'))
    keyboard.row(KeyboardButton(text='Help'))
    return keyboard.as_markup(resize_keyboard=True)

def make_searching_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Stop search', callback_data='stop_search')
    return keyboard.as_markup()