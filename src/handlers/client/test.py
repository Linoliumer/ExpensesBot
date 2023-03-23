from create_bot import *


@dp.message_handler()
async def test(message: types.Message) -> None:
    await message.answer("HELLO")