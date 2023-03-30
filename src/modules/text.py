from .file import File


class Text_App:
    menus = {}
    input = {}
    messages = {}
    errors = {}
    steps = {}

    def __init__(self, obj: File):
        self.formed_menus_text(obj.text)
        self.formed_input_text(obj.text)
        self.formed_messages_text(obj.text)
        self.formed_errors_text(obj.text)
        self.formed_steps_text(obj.text)

    def formed_menus_text(self, text: dict) -> None:
        for element in text['MENU']['TITLES']:
            self.menus[element] = f"{text['MENU']['HEADER'][element]}\n\n{text['MENU']['BODY'][element]}"

    def formed_input_text(self, text: dict) -> None:
        for key, value in text['INPUT'].items():
            self.input[key] = value

    def formed_messages_text(self, text: dict) -> None:
        for key, value in text['MESSAGE'].items():
            self.messages[key] = value

    def formed_errors_text(self, text: dict) -> None:
        for key, value in text['ERROR'].items():
            self.errors[key] = value

    def formed_steps_text(self, text: dict) -> None:
        for key, value in text['STEPS'].items():
            self.steps[key] = value
