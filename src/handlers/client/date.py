import datetime
from aiogram.dispatcher import FSMContext
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from create_bot import *
from aiogram.dispatcher.filters import ChatTypeFilter
from states.state import Cashless, Cash
from aiogram.dispatcher.filters import Text


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="entry_date:"),
    state=[Cashless.Date, Cash.Date]
)
async def simple_date(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Response to the Telegram server
    await callback.answer()
    # Get current day
    now = datetime.datetime.now()
    # Retrieving a command from a callback
    command = str(callback.data).split(':')[1]
    state_now = await state.get_state()
    if state_now == "Cashless:Date":
        await Cashless.Amount.set()
    else:
        await Cash.Amount.set()
    if command == "today":
        await state.update_data(date=f"{now.strftime('%d.%m.%Y')}")
    else:
        past = now - datetime.timedelta(days=1)
        await state.update_data(date=f"{past.strftime('%d.%m.%Y')}")
    await callback.message.answer(
        text=client_text.steps["AMOUNT"]
    )
    scheduler.reschedule_job(
        job_id=f"{callback.from_user.id}",
        trigger="date",
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=INPUT_TIME_AFK),
    )


# Calling calendar. Creating a new record. Step 1
@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    text="calendar",
    state=[Cashless.Date, Cash.Date]
)
async def calendar(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text=client_text.steps["DATE"],
        reply_markup=await SimpleCalendar().start_calendar()
    )
    scheduler.reschedule_job(
        job_id=f"{callback.from_user.id}",
        trigger="date",
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=INPUT_TIME_AFK),
    )


@dp.callback_query_handler(ChatTypeFilter(types.ChatType.PRIVATE), simple_cal_callback.filter(), state="*")
async def set_date(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:  # Data successfully obtained
        # Set date
        await state.update_data(date=f"{date.strftime('%d.%m.%Y')}")
        state_now = await state.get_state()
        if state_now == "Cashless:Date":
            await Cashless.Amount.set()
        else:
            await Cash.Amount.set()
        await callback.message.answer(
            text=client_text.steps["AMOUNT"]
        )
    scheduler.reschedule_job(
        job_id=f"{callback.from_user.id}",
        trigger="date",
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=INPUT_TIME_AFK),
    )