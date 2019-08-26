from flask import Blueprint
from flask_restful import Resource, Api


class User(Resource):
    def get(self):
        return {'msg': 'User GET resource'}

    def post(self):
        return {'msg': 'User POST resource'}


class UserProfile(Resource):
    def get(self, id):
        return {'msg': f'Get user id: {id}'}

    def put(self, id):
        return {'msg': f'Update user id: {id}'}

    def delete(self, id):
        return {'msg': f'Delete user id: {id}'}


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

user_api = Api(user_bp)
user_api.add_resource(User, '/')
user_api.add_resource(UserProfile, '/<int:id>/')
