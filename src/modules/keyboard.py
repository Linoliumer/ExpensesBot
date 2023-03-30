from aiogram import types

from modules import File


class Keyboard_App:

    keyboards = {}
    cash = {}
    cashless = {}

    def __init__(self, obj: File, obj_cfg: File):
        self.formed_keyboards(obj.text)
        self.formed_selection_keyboards(obj_cfg.text)

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

    def formed_selection_keyboards(self, text: dict):
        for element in text["CASH"]:
            keyboard = []
            len_elements = len(text["CASH"][element])
            overflow = len_elements % 2
            temp = len_elements - overflow
            name = element.lower()
            for i in range(0, temp, 2):
                print(i)
                line = [
                    types.InlineKeyboardButton(
                        text=text["CASH"][element][i], callback_data=f"{name}:{i}"
                    ),
                    types.InlineKeyboardButton(
                        text=text["CASH"][element][i+1], callback_data=f"{name}:{i+1}"
                    )
                ]
                keyboard.append(line)
            if overflow == 1:
                keyboard.append(
                    [
                        types.InlineKeyboardButton(
                        text=text["CASH"][element][temp], callback_data=f"{name}:{temp}"
                        )
                    ]
                )
            self.cash[element] = types.InlineKeyboardMarkup(
                resize_keyboard=True,
                inline_keyboard=keyboard
            )
        for element in text["CASHLESS"]:
            keyboard = []
            len_elements = len(text["CASHLESS"][element])
            overflow = len_elements % 2
            temp = len_elements - overflow
            name = element.lower()
            for i in range(0, temp, 2):
                print(i)
                line = [
                    types.InlineKeyboardButton(
                        text=text["CASHLESS"][element][i], callback_data=f"{name}:{i}"
                    ),
                    types.InlineKeyboardButton(
                        text=text["CASHLESS"][element][i+1], callback_data=f"{name}:{i+1}"
                    )
                ]
                keyboard.append(line)
            if overflow == 1:
                keyboard.append(
                    [
                        types.InlineKeyboardButton(
                        text=text["CASHLESS"][element][temp], callback_data=f"{name}:{temp}"
                        )
                    ]
                )
            self.cashless[element] = types.InlineKeyboardMarkup(
                resize_keyboard=True,
                inline_keyboard=keyboard
            )
