from aiogram.dispatcher.filters import ChatTypeFilter
from create_bot import *


@dp.callback_query_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=None)
async def unknown_callback_handler(call: types.CallbackQuery) -> None:
    await call.message.answer(
        text=client_text.messages["UNREGISTER"]
    )
    await call.answer()


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=None)
async def unknown_message_handler(message: types.Message) -> None:
    await message.answer(
        text=client_text.messages["UNREGISTER"]
    )


@dp.callback_query_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=[UserCondition.Owner, UserCondition.Staff])
async def known_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        text=client_text.messages["UNIDENTIFIED"]
    )
    await callback.answer()


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=[UserCondition.Owner, UserCondition.Staff])
async def known_message_handler(message: types.Message):
    await message.answer(
        text=client_text.messages["UNIDENTIFIED"]
    )


@dp.callback_query_handler(ChatTypeFilter(types.ChatType.PRIVATE), state="*")
async def answer(callback: types.CallbackQuery):
    await callback.answer()

