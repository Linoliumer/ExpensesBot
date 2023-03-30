from create_bot import *


async def error_menu(
        text: str,
        keyboard: types.InlineKeyboardMarkup,
        callback: types.CallbackQuery = None,
        message: types.Message = None,
) -> None:
    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message

    await obj_for_answer.answer(
        text=text,
        reply_markup=keyboard
    )


async def menu_owner(callback: types.CallbackQuery = None, message: types.Message = None) -> None:

    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message

    await obj_for_answer.answer(
        text=client_text.menus["MENU_OWNER"].format(
            fConfig.text["SPREADSHEET"]["SET_ID"],
            await cashless_url(),
            await cash_url()
        ),
        reply_markup=keyboard.keyboards["MENU_OWNER"]
    )


async def menu_staff(callback: types.CallbackQuery = None, message: types.Message = None) -> None:

    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message

    await obj_for_answer.answer(
        text=client_text.menus["MENU_STAFF"],
        reply_markup=keyboard.keyboards["MENU_STAFF"]
    )


async def select_type(callback: types.CallbackQuery = None, message: types.Message = None) -> None:
    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message

    await obj_for_answer.answer(
        text=client_text.menus["SELECT_TYPE_ENTRY"],
        reply_markup=keyboard.keyboards["SELECT_TYPE_ENTRY"]
    )


async def settings_menu(callback: types.CallbackQuery = None, message: types.Message = None) -> None:
    if callback is None:
        # If the function is called by the trigger on the message
        obj_for_answer = message
    else:
        # If the function is called callback
        obj_for_answer = callback.message

    await obj_for_answer.answer(
        text=client_text.menus["SETTINGS"],
        reply_markup=keyboard.keyboards["SETTINGS"]
    )
