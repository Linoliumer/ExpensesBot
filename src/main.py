import uvicorn
from fastapi import FastAPI
from create_bot import *
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from models import User
from middlewares import Determination
from handlers import *
app = FastAPI()


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url=f"sqlite://{BASE_DIR}{DATABASE_PATH}",
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


@app.on_event("startup")
async def on_startup():
    dp.middleware.setup(Determination())
    await init()
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
    await session.close()
    await Tortoise.close_connections()


if __name__ == "__main__":
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT)