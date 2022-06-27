# Online Chess Telegram bot

## Features

- ##### Enemy search system
- ##### Player statistics
- ##### PostgresSQL and Redis (WIP) support
- ##### Leaderboard
- ##### ELO rating system
- ##### Full asynchronous support

## Libraries used
- [Aiogram](https://github.com/aiogram/aiogram)
- [Pillow](https://github.com/python-pillow/Pillow)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

## Installation

Grab ```.env.dist``` file, rename it to ```.env```
```sh
git clone https://github.com/1nv4510n/chess_bot.git
cd chess_bot
pip install -r requirements.txt
python bot.py
```

## Environments setup
```BOT_TOKEN``` - Telegram bot token  
```BOT_FSM_STORAGE``` - ```memory``` or ```redis``` storage  
```POSTGRES_DSN``` - PostgresSQL Data Source Name