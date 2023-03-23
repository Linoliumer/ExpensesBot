from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=50)
    # 0 - Staff, 1 - Admin
    role = fields.IntField()

