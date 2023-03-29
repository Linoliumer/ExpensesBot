from aiogram.dispatcher import FSMContext
from create_bot import *


async def set_spreadsheet(callback: types.CallbackQuery, state: FSMContext):
    await Input.Spreadsheet_id.set()
    await callback.message.answer(
        text=client_text.input["SPREADSHEET_ID"]
    )

