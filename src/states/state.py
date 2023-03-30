from aiogram.dispatcher.filters.state import StatesGroup, State


class UserCondition(StatesGroup):
    Owner = State()
    Staff = State()
    Unregister = State()


class Input(StatesGroup):
    Spreadsheet_id = State()


class CashEntry(StatesGroup):
    pass


class Cashless(StatesGroup):
    Date = State()
    Calendar = State()
    Amount = State()
    SourcePayment = State()
    Category = State()
    Commentary = State()
    Accept = State()
    Finish = State()


class Cash(StatesGroup):
    Date = State()
    Calendar = State()
    Amount = State()
    Category = State()
    Commentary = State()
    Accept = State()
    Finish = State()








