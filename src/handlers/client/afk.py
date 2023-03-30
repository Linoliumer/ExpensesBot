from create_bot import *
from aiogram.dispatcher import FSMContext


async def afk(state: FSMContext, message: types.Message = None, callback: types.CallbackQuery = None) -> None:
    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message
    try:
        await state.finish()
    except Exception as e:
        logging.error(f"State.\nError: {str(e)}", exc_info=True)
    await obj_for_answer.answer(
        text=client_text.messages["AFK"]
    )

