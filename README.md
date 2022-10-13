# Online Chess Telegram bot

## Features

- ##### Enemy search system
- ##### Player statistics
- ##### PostgreSQL and Redis (WIP) support
- ##### Leaderboard
- ##### ELO rating system
- ##### Full asynchronous support

## Libraries used
- [Aiogram](https://github.com/aiogram/aiogram)
- [Pillow](https://github.com/python-pillow/Pillow)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [pydantic](https://github.com/samuelcolvin/pydantic)

## Installation

Grab ```env-example``` file, rename it to ```.env```
```sh
git clone https://github.com/1nv4510n/telegram-chess-bot.git
cd telegram-chess-bot
pip install -r requirements.txt
python bot.py
```

## Environments setup
```BOT_TOKEN``` - Telegram bot token  
```BOT_FSM_STORAGE``` - ```memory``` or ```redis``` (WIP) storage  
```POSTGRES_DSN``` - PostgreSQL Data Source Name
