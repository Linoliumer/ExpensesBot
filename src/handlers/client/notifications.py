from create_bot import *
from models import Chat, User


async def notification_owner_chats(data, sender: int) -> None:
    try:
        owners = await User.filter(role=1)
        chats = await Chat.all()
    except Exception as e:
        logging.error(f"Database error.\nError: {str(e)}", exc_info=True)
        return
    if data["type"] == "CASHLESS":
        url_table = await cashless_url()
    else:
        url_table = await cash_url()
    ids = [owner.telegram_id for owner in owners]
    for chat in chats:
        ids.append(chat.telegram_chat_id)
    ids.remove(sender)
    for id in ids:
        print(id)
        try:
            await dp.bot.send_message(
                chat_id=id,
                text=client_text.messages["CHAT_NOTIFICATION"].format(
                    data["preview"], url_table
                )
            )
        except Exception as e:
            pass
