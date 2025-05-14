from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..backend import get_excel_report

get_report_router = Router()


@get_report_router.callback_query(F.data == 'download_results')
async def download_report_handler(callback: CallbackQuery, state: FSMContext):
    excel_report = await get_excel_report()
    await callback.message.answer_document(excel_report, caption='Отчет')
