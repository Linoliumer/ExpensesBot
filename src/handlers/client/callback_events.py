from aiogram.dispatcher import FSMContext
from create_bot import *
from aiogram.dispatcher.filters import ChatTypeFilter
from handlers.client.menu import menu_owner, menu_staff, select_type, error_menu, settings_menu
from aiogram.dispatcher.filters import Text

from handlers.client.spreadsheet_id import input_spreadsheetId


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    text="menu",
    state=[UserCondition.Owner, UserCondition.Staff]
)
async def menu_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Response to the Telegram server
    await callback.answer()
    state_now = await state.get_state()
    if state_now == "UserCondition:Owner":
        await menu_owner(callback=callback)
    elif state_now == "UserCondition:Staff":
        await menu_staff(callback=callback)


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="menu:"),
    state=UserCondition.Owner
)
async def menu_process_callback(callback: types.CallbackQuery) -> None:
    # Response to the Telegram server
    await callback.answer()
    # Retrieving a command from a callback
    command = str(callback.data).split(':')[1]
    if command == "add_entry":
        if fConfig.text["SPREADSHEET"]["SET_ID"] != 0:
            await select_type(callback=callback)
        else:
            # Calling the error menu
            await error_menu(
                text=client_text.errors["SPREADSHEET_NOT_SET"],
                keyboard=keyboard.keyboards["IN_MENU"],
                callback=callback
            )
    elif command == "settings":
        await settings_menu(callback=callback)
    else:
        # Calling the error menu
        await error_menu(
            text=client_text.errors["ERROR"],
            keyboard=keyboard.keyboards["IN_MENU"],
            callback=callback
        )


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="settings:"),
    state=UserCondition.Owner
)
async def settings_process_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Response to the Telegram server
    await callback.answer()
    # Retrieving a command from a callback
    command = str(callback.data).split(':')[1]
    if command == "set_spreadsheet":
        await input_spreadsheetId(callback=callback, state=state)
    else:
        # Calling the error menu
        await error_menu(
            text=client_text.errors["ERROR"],
            keyboard=keyboard.keyboards["SETTINGS"],
            callback=callback
        )

