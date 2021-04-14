from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    """ Model user """
    id = fields.data.UUIDField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)

    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100, null=True)

    date_join = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)

    is_active = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ('password',)


UserDB = pydantic_model_creator(User, name="UserDB", exclude_readonly=True)
