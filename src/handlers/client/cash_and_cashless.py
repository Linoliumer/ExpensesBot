from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import *
from aiogram.dispatcher.filters import ChatTypeFilter

from handlers.client.menu import menu_owner, menu_staff
from models import User
from spreadsheet import add_entry
from states.state import Cashless, Cash


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    text="add_entry:cash",
    state=[UserCondition.Owner, UserCondition.Staff]
)
async def cash_start(callback: types.CallbackQuery) -> None:
    # Response to the Telegram server
    await callback.answer()
    await Cash.Date.set()
    await callback.message.answer(
        text=client_text.steps["DATE"],
        reply_markup=keyboard.keyboards["SELECT_DATE"]
    )


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    text="add_entry:cashless",
    state=UserCondition.Owner
)
async def cashless_start(callback: types.CallbackQuery) -> None:
    # Response to the Telegram server
    await callback.answer()
    await Cashless.Date.set()
    await callback.message.answer(
        text=client_text.steps["DATE"],
        reply_markup=keyboard.keyboards["SELECT_DATE"]
    )


@dp.message_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    state=[Cashless.Amount, Cash.Amount]
)
async def set_amount(message: types.Message, state: FSMContext):
    try:
        # Converting amount to float
        amount = float(message.text)
        # Verification amount
        if amount <= 0:
            raise Exception
    except Exception as e:
        logging.error(f"Validation.\nError: {str(e)}", exc_info=True)
        await message.answer(
            text=client_text.errors["AMOUNT_VALIDATION"]
        )
        await message.answer(
            text=client_text.steps["AMOUNT"]
        )
        return
    # Saving temporary data
    await state.update_data(amount=amount)
    state_now = await state.get_state()
    if state_now == "Cashless:Amount":
        await Cashless.SourcePayment.set()
        await message.answer(
            text=client_text.steps["SOURCES"],
            reply_markup=keyboard.cashless["SOURCES"]
        )
    else:
        await Cash.Category.set()
        await message.answer(
            text=client_text.steps["CATEGORY"],
            reply_markup=keyboard.cash["CATEGORY"]
        )


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="sources:"),
    state=Cashless.SourcePayment
)
async def set_source(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await Cashless.Category.set()
    # Split callback
    result = int(str(callback.data).split(':')[1])
    # Set source
    await state.update_data(sourcepayment=fConfig.text["CASHLESS"]["SOURCES"][result])
    await callback.message.answer(
        text=client_text.steps["CATEGORY"],
        reply_markup=keyboard.cashless["CATEGORY"]
    )


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="category:"),
    state=[Cash.Category, Cashless.Category]
)
async def set_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    state_now = await state.get_state()
    if state_now == "Cashless:Category":
        element = "CASHLESS"
        await Cashless.Commentary.set()
    else:
        element = "CASH"
        await Cash.Commentary.set()
    # Split callback
    result = int(str(callback.data).split(':')[1])
    # Set category
    await state.update_data(category=fConfig.text[element]["CATEGORY"][result])
    await callback.message.answer(
        text=client_text.steps["COMMENTARY"]
    )


@dp.message_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    state=[Cash.Commentary, Cashless.Commentary]
)
async def set_commentary(message: types.Message, state: FSMContext):
    # Set author
    await state.update_data(
        comment=message.text,
        username=message.from_user.first_name,
    )
    # Get data
    data = await state.get_data()
    state_now = await state.get_state()
    if state_now == "Cashless:Commentary":
        await Cashless.Accept.set()
        preview = client_text.steps["TEMPLATE_CASHLESS"].format(
            "Безналичка", data["date"], data["amount"],
            data["sourcepayment"], data["category"], data["comment"],
            data["username"]
        )
        await state.update_data(
            type="CASHLESS",
            preview=preview
        )
    else:
        await Cash.Accept.set()
        preview = client_text.steps["TEMPLATE_CASH"].format(
            "Наличка", data["date"], data["amount"],
            data["category"], data["comment"], data["username"]
        )
        await state.update_data(
            type="CASH",
            preview=preview
        )
    await message.answer(
        text=preview,
        reply_markup=keyboard.keyboards["ADD_ENTRY"]
    )


@dp.callback_query_handler(
    ChatTypeFilter(types.ChatType.PRIVATE),
    Text(startswith="add_entry:"),
    state=[Cash.Accept, Cashless.Accept]
)
async def add_entry_accept(callback: types.CallbackQuery, state: FSMContext, user: User) -> None:
    # Get data
    await callback.answer()
    data = await state.get_data()
    result = str(callback.data).split(':')[1]
    if result == "accept":
        ok = await add_entry(service, fConfig.text, data)
        if ok:
            await callback.message.answer(
                text=client_text.messages["ADD_ENTRY_ACCEPT"]
            )
        else:
            await callback.message.answer(
                text=client_text.errors["ERROR"]
            )
    else:
        await callback.message.answer(
            text=client_text.messages["ADD_ENTRY_CANCEL"]
        )
    await state.finish()
    if user.role == 1:
        await menu_owner(callback=callback)
    elif user.role == 0:
        await menu_staff(callback=callback)