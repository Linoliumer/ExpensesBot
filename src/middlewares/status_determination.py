import logging
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from tortoise.exceptions import DoesNotExist

from create_bot import dp, client_text
from models import *
from states import *


unusual_states = ["Input:Spreadsheet_id"]

class Determination(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)
        try:
            user = await User.get(telegram_id=message.from_user.id)
        except DoesNotExist:
            pass
        except Exception as e:
            logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
            await message.answer(
                text=client_text.errors["ERROR"]
            )
            return
        else:
            state_now = await state.get_state()
            if state_now not in unusual_states:
                if user.role == 1:
                    await state.set_state(UserCondition.Owner)
                elif user.role == 0:
                    await state.set_state(UserCondition.Staff)
            data["user"] = user
        """
        state_now = await state.get_state()
        logging.info(f"{message.from_user.id} -- {state_now}")
        """

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        state = dp.current_state(chat=callback.from_user.id, user=callback.from_user.id)
        try:
            user = await User.get(telegram_id=callback.from_user.id)
        except DoesNotExist:
            pass
        except Exception as e:
            logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
            await callback.message.answer(
                text=client_text.errors["ERROR"]
            )
            return
        else:
            state_now = await state.get_state()
            if state_now not in unusual_states:
                if user.role == 1:
                    await state.set_state(UserCondition.Owner)
                elif user.role == 0:
                    await state.set_state(UserCondition.Staff)
            data["user"] = user
        """
        state_now = await state.get_state()
        logging.info(f"{message.from_user.id} -- {state_now}")
        """
