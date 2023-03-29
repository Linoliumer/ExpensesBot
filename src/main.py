import uvicorn
from fastapi import FastAPI
from create_bot import *
from handlers import *
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )
        logging.info("WEBHOOK SET")
    logging.info("WEBHOOK DETECTED")


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    session = await bot.get_session()
    # await session.close()


register_tortoise(
    app,
    db_url=f"sqlite://{BASE_DIR}/database/db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT)