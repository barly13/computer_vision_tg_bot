from aiogram.types import BufferedInputFile

from .computer_vision_reporter import ComputerVisionReporter


async def get_excel_report():
    bytes_output = await ComputerVisionReporter().generate_report()
    excel_report = BufferedInputFile(bytes_output, filename='Файл.xls')

    return excel_report
