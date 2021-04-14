from tortoise import fields, models
import binascii
import os


class Token(models.Model):
    """ Model user """
    user = fields.OneToOneField("models.User", on_delete=fields.CASCADE)
    created = fields.DatetimeField(auto_now_add=True)
    key = fields.CharField(default=binascii.hexlify(os.urandom(20)).decode(), max_length=40, primary_key=True)
