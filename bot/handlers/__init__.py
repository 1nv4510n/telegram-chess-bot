from aiogram import Router

from .users import users_router
from .errors import errors_router

router = Router()
router.include_router(users_router)
router.include_router(errors_router)