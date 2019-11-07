from marshmallow import fields

from fantasybooks_api import ma
from fantasybooks_api.models import User


class UserSchema(ma.ModelSchema):
    password = fields.String(load_only=True)
    avatar = fields.Function(lambda obj: obj.avatar(), dump_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'name',
            'surname',
            'email',
            'created_at',
            'updated_at',
            'last_activity',
            'is_admin',
            'avatar'
        )
