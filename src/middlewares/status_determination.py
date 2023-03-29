import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from create_bot import dp
from models import User
from states import *


class Determination(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)
        user = User(telegram_id=message.from_user.id)
        if user is None:
            await state.set_state(UserCondition.Unregister)
        elif user.role == 1:
            await state.set_state(UserCondition.Owner)
        elif user.role == 0:
            await state.set_state(UserCondition.Staff)
        data["user"] = user

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        state = dp.current_state(chat=callback.from_user.id, user=callback.from_user.id)
        user = User(telegram_id=callback.from_user.id)
        if user is None:
            await state.set_state(UserCondition.Unregister)
        elif user.role == 1:
            await state.set_state(UserCondition.Owner)
        elif user.role == 0:
            await state.set_state(UserCondition.Staff)
        data["user"] = user