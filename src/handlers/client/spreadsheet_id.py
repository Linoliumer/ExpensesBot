import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from create_bot import *
from handlers.client.afk import afk
from handlers.client.menu import error_menu, settings_menu
from spreadsheet import activate_spreadsheet


async def input_spreadsheetId(callback: types.CallbackQuery, state: FSMContext):
    await Input.Spreadsheet_id.set()
    await callback.message.answer(
        text=client_text.input["SPREADSHEET_ID"]
    )
    scheduler.add_job(
        id=f"{callback.from_user.id}",
        func=afk,
        trigger="date",
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=INPUT_TIME_AFK),
        args=(state, None, callback)
    )
    logging.info(f"Job input_spreadsheetId {callback.from_user.id} - start")


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), content_types=["text"], state=Input.Spreadsheet_id)
async def spreadsheet_set(message: types.Message, state: FSMContext):
    if len(message.text) <= SPREADSHEET_CHAT_LEN:
        await state.finish()
        scheduler.remove_job(job_id=f"{message.from_user.id}")
        ok = await activate_spreadsheet(spreadsheet_id=message.text)
        if ok:
            await message.answer(
                text=client_text.messages["ACTIVE_SPREADSHEET"]
            )
            await settings_menu(message=message)
            return
        await error_menu(
            text=client_text.errors["ERROR"],
            keyboard=keyboard.keyboards["SETTINGS"],
            message=message
        )
    else:
        await message.answer(
            text=client_text.errors["SPREADSHEET_LEN"]
        )
