from aiogram.dispatcher import FSMContext

from create_bot import *
from aiogram.dispatcher.filters import ChatTypeFilter


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["set"], state="*")
async def test_set(message: types.Message) -> None:
    await message.answer(
        text=f"""SET_ID={fConfig.text['SPREADSHEET']['SET_ID']}
SPREADSHEET_ID={fConfig.text['SPREADSHEET']['SPREADSHEET_ID']}
CASH_ID={fConfig.text['SPREADSHEET']['CASH_ID']}
CASHLESS_ID={fConfig.text['SPREADSHEET']['CASHLESS_ID']}"""
    )


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["state"], state="*")
async def test_state(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(
        text=str(data)
    )