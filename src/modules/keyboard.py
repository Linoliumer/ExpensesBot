from aiogram import types

from modules import File


class Keyboard_App:

    keyboards = {}

    def __init__(self, obj: File):
        self.formed_keyboards(obj.text)

    def formed_keyboards(self, text: dict):
        for element in text:
            keyboard = []
            for line in text[element]:
                line_buttons = []
                for button in line:
                    if button["type"] == "callback":
                        line_buttons.append(
                            types.InlineKeyboardButton(text=button["text"], callback_data=button["data"])
                        )
                    else:
                        line_buttons.append(
                            types.InlineKeyboardButton(text=button["text"], url=button["data"])
                        )
                keyboard.append(line_buttons)
            self.keyboards[element] = types.InlineKeyboardMarkup(
                resize_keyboard=True,
                inline_keyboard=keyboard
            )