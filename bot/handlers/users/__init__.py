from aiogram import Router

from .chess import router as chess_router
from .default import router as default_router
from .leaderboard import router as leaderboard_router
from .search_game import router as search_game_router
from .statistics import router as statistics_router

users_router = Router()
users_router.include_router(chess_router)
users_router.include_router(default_router)
users_router.include_router(leaderboard_router)
users_router.include_router(search_game_router)
users_router.include_router(statistics_router)
