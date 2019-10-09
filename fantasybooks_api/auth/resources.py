from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import EXCLUDE

from fantasybooks_api.models import User
from fantasybooks_api.schemas import UserSchema
from fantasybooks_api.utils import handle_sqlalchemy_error


class UserResource(Resource):
    def get(self):
        return {'users': UserSchema(many=True).dump(User.all())}, 200

    def post(self):
        new_user = UserSchema().load(request.get_json())
        try:
            new_user.save()
        except SQLAlchemyError as error:
            return {'msg': handle_sqlalchemy_error(error)}, 400
        return {'msg': 'User created', 'user_id': new_user.id}, 201


class UserProfile(Resource):
    def get(self, id):
        user = User.get(id)
        if user:
            return {'user': UserSchema().dump(user)}, 200
        return {'msg': 'User not found!'}, 404

    def put(self, id):
        user = User.get(id)
        if not user:
            return {'msg': 'User not found!'}, 404

        non_update_fields = ('id', 'username', 'email')
        user = UserSchema(exclude=non_update_fields, unknown=EXCLUDE).load(
            request.get_json(), instance=user
        )
        user.save()

        return {'msg': f'User updated!'}, 200

    def delete(self, id):
        try:
            User.delete(id)
        except RuntimeError as error:
            return {'msg': str(error)}, 400
        except SQLAlchemyError as error:
            return {'msg': handle_sqlalchemy_error(error)}, 400

        return {'msg': 'User deleted!'}, 200


user_bp = Blueprint('user_bp', __name__)

user_api = Api(user_bp)
user_api.add_resource(UserResource, '/user')
user_api.add_resource(UserProfile, '/user/<string:id>')
