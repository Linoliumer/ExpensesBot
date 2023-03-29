from aiogram.dispatcher import FSMContext
from create_bot import *
from models import User


async def enter_password(
        call: types.CallbackQuery = None,
        message: types.Message = None,
        state: FSMContext = None,
        user: User = None
) -> None:

    # Calling the desired state
    await Input.Password.set()

    if call is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = call.message

    await obj_for_answer.answer(
        text=client_text.input["PASSWORD"]
    )