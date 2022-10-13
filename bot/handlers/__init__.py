from aiogram import Router

from .users import users_router

router = Router()
router.include_router(users_router)
