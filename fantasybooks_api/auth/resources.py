from datetime import datetime

from flask import Blueprint, current_app, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_jwt_identity,
    jwt_refresh_token_required,
    jwt_required,
)
from flask_restful import Api, Resource
from marshmallow import EXCLUDE
from sqlalchemy.exc import SQLAlchemyError

from fantasybooks_api.models import User
from fantasybooks_api.schemas import UserSchema
from fantasybooks_api.utils import handle_sqlalchemy_error


class UserResource(Resource):
    @jwt_required
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

    @jwt_required
    def put(self, id):
        user = User.get(id)
        if not user:
            return {'msg': 'User not found!'}, 404

        non_update_fields = ('id', 'username', 'email', 'is_admin')
        user = UserSchema(exclude=non_update_fields, unknown=EXCLUDE).load(
            request.get_json(), instance=user
        )
        user.save()

        return {'msg': f'User updated!'}, 200

    @jwt_required
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


class LoginResource(Resource):
    def post(self):
        if not request.is_json:
            return {'msg': 'Missing JSON in request'}, 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return {'msg': 'Missing username parameter'}, 400
        if not password:
            return {'msg': 'Missing password parameter'}, 400

        from fantasybooks_api.models import User

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {'msg': 'Bad username or password'}, 401

        from fantasybooks_api import redis

        now = datetime.utcnow()

        access_token = create_access_token(identity=username)
        access_then = now - current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        redis.set(
            get_jti(encoded_token=access_token),
            'false',
            (now - access_then).seconds * 1.2,
        )

        refresh_token = create_refresh_token(identity=username)
        refresh_then = now - current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        redis.set(
            get_jti(encoded_token=refresh_token),
            'false',
            (now - refresh_then).seconds * 1.2,
        )

        return ({'access_token': access_token, 'refresh_token': refresh_token}, 200)


class TokenRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        return {'access_token': create_access_token(identity=get_jwt_identity())}, 200


auth_bp = Blueprint('auth_bp', __name__)

auth_api = Api(auth_bp)
auth_api.add_resource(LoginResource, '/login')
auth_api.add_resource(TokenRefreshResource, '/login/refresh')
