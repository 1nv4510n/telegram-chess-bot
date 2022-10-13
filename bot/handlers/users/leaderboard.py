from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import Text, Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.filters.search_filter import UserPlayingFilter, UserSearchingFilter

from bot.db.models import PlayersEntry
from bot.db.requests import get_top_users, get_leaderboard_position, get_user_rating

router = Router()

@router.message(UserPlayingFilter(playing=False), UserSearchingFilter(searching=False), Text('Leaderboard'))
@router.message(UserPlayingFilter(playing=False), UserSearchingFilter(searching=False), Command('top'))
async def command_top(message: Message, session: AsyncSession):
    users = await get_top_users(session)
    
    text = f"<b>TOP {len(users)} PLAYERS BY RATING</b>\n\n"
    
    i = 1
    current_user_in_top: bool = False
    user: PlayersEntry
    for user in users:
        if user.telegram_id == message.from_user.id:
            text += html.underline(f"<b>{i}. {message.from_user.first_name} (You) rating: {round(user.rating)}</b>\n")
            current_user_in_top = True
        else:
            if i % 2 != 0:
                text += f"{i}. {user.name} rating: {round(user.rating)}\n"
            else:
                text += html.bold(f"{i}. {user.name} rating: {round(user.rating)}\n")
        i += 1
        
    if not current_user_in_top:
        rating = await get_user_rating(session, message.from_user.id)
        pos = await get_leaderboard_position(session, message.from_user.id)
        text += '...\n' + html.underline(f"<b>{pos}. {message.from_user.first_name} (You) rating: {round(rating)}</b>")
    
    await message.answer(text=text)