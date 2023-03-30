from aiogram.dispatcher import FSMContext
from create_bot import *
from aiogram.dispatcher.filters import ChatTypeFilter
from models import User
from handlers.client.menu import menu_owner, menu_staff
from states.state import Cash, Cashless


@dp.message_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    commands=["cancel"],
    state=[Input.Spreadsheet_id, Cash, Cashless]
)
async def cancel(message: types.Message, state: FSMContext, user: User) -> None:
    try:
        scheduler.remove_job(job_id=f"{message.from_user.id}")
    except Exception as e:
        logging.info(f"Scheduler.\nError: {str(e)}", exc_info=True)
    try:
        await state.finish()
    except Exception as e:
        logging.info(f"State.\nError: {str(e)}", exc_info=True)
    if user.role == 1:
        await menu_owner(message=message)
    elif user.role == 0:
        await menu_staff(message=message)


@dp.message_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    commands=["start", "menu"],
    state=[UserCondition.Owner, UserCondition.Staff]
)
async def menu_message_handler(message: types.Message, state: FSMContext):
    state_now = await state.get_state()
    if state_now == "UserCondition:Owner":
        await menu_owner(message=message)
    elif state_now == "UserCondition:Staff":
        await menu_staff(message=message)


@dp.message_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    commands="pass",
    state=None
)
async def sing_up(message: types.Message):
    command = (str(message.text).split(' '))
    if len(command) == 2:
        password = command[1]
        if password == fConfig.text["PASSWORD"]["OWNER"]:
            role = 1
        elif password == fConfig.text["PASSWORD"]["STAFF"]:
            role = 0
        else:
            await message.answer(
                text=client_text.errors["INVALID_PASSWORD"]
            )
            return
        try:
            await User.create(
                telegram_id=message.from_user.id,
                role=role
            )
        except Exception as e:
            logging.error(f"Database error:\n{str(e)}", exc_info=True)
            await message.answer(
                text=client_text.errors["ERROR"]
            )
            return
        await message.answer(
            text=client_text.messages["SUCCESS_AUTH"]
        )
    else:
        await message.answer(
            text=client_text.errors["INVALID_COMMAND"]
        )

