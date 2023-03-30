from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    # 0 - Staff, 1 - Owner
    role = fields.IntField()


class SpreadsheetSet(Model):
    id = fields.IntField(pk=True)
    spreadsheet_id = fields.CharField(max_length=100)
    cashless_id = fields.IntField()
    cash_id = fields.IntField()
    active = fields.BooleanField(default=True)


class Chat(Model):
    id = fields.IntField(pk=True)
    telegram_chat_id = fields.IntField(unique=True)