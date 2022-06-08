from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command="start", description="Play chess!"),
                BotCommand(command="new_game", description="Search game"),
                BotCommand(command="resign", description="Resign the game"),
                BotCommand(command="stats", description="Your personal statistics."),
                BotCommand(command="top", description="Show leaderboard"),
                BotCommand(command="help", description="How to play chess?")
            ],
            BotCommandScopeAllPrivateChats(),
            None
        )
    ]
    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)