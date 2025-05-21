from aiogram import Router

from .handlers import analysis_methods_router

base_analysis_methods_router = Router()
base_analysis_methods_router.include_routers(
    analysis_methods_router
)