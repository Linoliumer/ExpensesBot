import uvicorn
from fastapi import FastAPI
from create_bot import *
from tortoise import Tortoise
from middlewares import Determination
from handlers import *


app = FastAPI()


"""----------SPREADSHEET_SET----------"""


async def init() -> None:
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url=f"sqlite://{BASE_DIR}{DATABASE_PATH}",
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def spreadsheet_set_detect() -> None:
    try:
        spreadsheet_set = await SpreadsheetSet.get(active=True)
    except DoesNotExist:
        fConfig.text["SPREADSHEET"]["SPREADSHEET_ID"] = "None"
        fConfig.text["SPREADSHEET"]["CASH_ID"] = 0
        fConfig.text["SPREADSHEET"]["CASHLESS_ID"] = 0
        fConfig.text["SPREADSHEET"]["SET_ID"] = 0
    except Exception as e:
        logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
        await on_shutdown()
    else:
        fConfig.text["SPREADSHEET"]["SPREADSHEET_ID"] = spreadsheet_set.spreadsheet_id
        fConfig.text["SPREADSHEET"]["CASH_ID"] = spreadsheet_set.cash_id
        fConfig.text["SPREADSHEET"]["CASHLESS_ID"] = spreadsheet_set.cashless_id
        fConfig.text["SPREADSHEET"]["SET_ID"] = spreadsheet_set.id


@app.on_event("startup")
async def on_startup():
    scheduler.start()
    await init()
    await spreadsheet_set_detect()
    dp.middleware.setup(Determination())
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
