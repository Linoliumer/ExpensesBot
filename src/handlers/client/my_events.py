from create_bot import *
from models import Chat, User


# Events bot
@dp.my_chat_member_handler()
async def my_chat_member(event: types.ChatMemberUpdated) -> None:
    if event["old_chat_member"]["status"] == "left":
        if event["new_chat_member"]["status"] == "member":
            try:
                user = await User.get(telegram_id=event['from']['id'])
            except DoesNotExist:
                await bot.send_message(chat_id=event["chat"]["id"], text=client_text.errors["CHAR_EVENER_NOT_OWNER"])
                await bot.leave_chat(event["chat"]["id"])
                return
            except Exception as e:
                logging.error(f"1 Error: {str(e)}", exc_info=True)
                await bot.send_message(chat_id=event["chat"]["id"], text=client_text.errors["ERROR"])
                await bot.leave_chat(event["chat"]["id"])
                return
            if user.role == 1:
                try:
                    await Chat.get(telegram_chat_id=event["chat"]["id"])
                except DoesNotExist:
                    await Chat.create(telegram_chat_id=event["chat"]["id"])
                except Exception as e:
                    logging.error(f"2 Error: {str(e)}", exc_info=True)
                    await bot.send_message(chat_id=event["chat"]["id"], text=client_text.errors["ERROR"])
                    await bot.leave_chat(event["chat"]["id"])
                    return
                await bot.send_message(chat_id=event["chat"]["id"], text=client_text.messages["CHAT_NOTIFICATION_ENTER"])
            else:
                await bot.send_message(chat_id=event["chat"]["id"], text=client_text.errors["CHAR_EVENER_NOT_OWNER"])
                await bot.leave_chat(event["chat"]["id"])
    elif event["old_chat_member"]["status"] == "member":
        if event["new_chat_member"]["status"] == "left":
            try:
                # Bot kicked from chat
                chat = await Chat.get(telegram_chat_id=event["chat"]["id"])
            except Exception as e:
                logging.error(f"Error: {str(e)}", exc_info=True)
                return
            await chat.delete()
