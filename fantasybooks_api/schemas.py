from fantasybooks_api import ma
from fantasybooks_api.models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
