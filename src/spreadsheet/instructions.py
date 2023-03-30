import logging
from tortoise.exceptions import DoesNotExist
from models import SpreadsheetSet
from create_bot import fConfig, service
from spreadsheet.requests import add_sheets


async def deactivate_spreadsheet() -> bool:
    try:
        spreadsheet_active = await SpreadsheetSet.get(active=True)
    except DoesNotExist:
        return True
    except Exception as e:
        logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
        return False
    else:
        spreadsheet_active.active = False
        try:
            await spreadsheet_active.save()
        except Exception as e:
            logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
            return False
        return True


async def create_spreadsheet(spreadsheet_id: str):
    data = {}
    data["SPREADSHEET_ID"] = spreadsheet_id
    data["SET_ID"] = 0
    data = await add_sheets(service, data)
    return await SpreadsheetSet(
        spreadsheet_id=data["SPREADSHEET_ID"],
        cashless_id=data["CASHLESS_ID"],
        cash_id=data["CASH_ID"],
        active=True
    )


async def activate_spreadsheet(spreadsheet_id: str) -> bool:
    ok = await deactivate_spreadsheet()
    if ok:
        try:
            spreadsheet = await SpreadsheetSet.get(spreadsheet_id=spreadsheet_id)
        except DoesNotExist:
            spreadsheet = await create_spreadsheet(spreadsheet_id=spreadsheet_id)
        except Exception as e:
            logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
            return False
        spreadsheet.active = True
        try:
            await spreadsheet.save()
        except Exception as e:
            logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
            return False
        fConfig.text["SPREADSHEET"]["SPREADSHEET_ID"] = spreadsheet.spreadsheet_id
        fConfig.text["SPREADSHEET"]["CASH_ID"] = spreadsheet.cash_id
        fConfig.text["SPREADSHEET"]["CASHLESS_ID"] = spreadsheet.cashless_id
        fConfig.text["SPREADSHEET"]["SET_ID"] = spreadsheet.id
        return True
    return False
