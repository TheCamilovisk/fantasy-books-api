from marshmallow import fields

from fantasybooks_api import ma
from fantasybooks_api.models import User


class UserSchema(ma.ModelSchema):
    password = fields.String(load_only=True)

    class Meta:
        model = User
