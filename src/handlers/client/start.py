from create_bot import *
from aiogram.dispatcher import FSMContext
from handlers.client.enter_password import enter_password
from models import User
from aiogram.dispatcher.filters import ChatTypeFilter


@dp.callback_query_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=UserCondition.Unregister)
async def start_callback_handler(call: types.CallbackQuery, state: FSMContext, user: User) -> None:
    await call.answer()
    await enter_password(call=call, state=state, user=user)