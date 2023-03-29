from aiogram.dispatcher.filters.state import StatesGroup, State


class UserCondition(StatesGroup):
    Owner = State()
    Staff = State()
    Unregister = State()


class Input(StatesGroup):
    Password = State()











