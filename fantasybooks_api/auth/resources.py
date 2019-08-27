from flask import Blueprint, request
from flask_restful import Resource, Api
from uuid import uuid4


mock_users = [
    {
        'id': str(uuid4()),
        'username': 'username0',
        'name': 'User',
        'surname': '0',
        'email': 'user0@example.com',
        'created_at': '2019-08-06 20:54:47.051355',
        'updated_at': '2019-08-16 20:54:47.051355',
        'last_activity': '2019-08-17 20:54:47.051355',
    },
    {
        'id': str(uuid4()),
        'username': 'username1',
        'name': 'User',
        'surname': '1',
        'email': 'user1@example.com',
        'created_at': '2019-08-10 20:54:47.051468',
        'last_activity': '2019-08-14 20:54:47.051468',
    },
]


def create_user(user_dict):
    global mock_users
    user_dict['id'] = str(uuid4())
    mock_users.append(user_dict)
    return mock_users[-1]


def find_user(id):
    for user in mock_users:
        if user['id'] == id:
            return user
    return None


def delete_user(id):
    for user in mock_users:
        if user['id'] == id:
            mock_users.remove(user)
            return True
    return False


class User(Resource):
    def get(self):
        return {'users': mock_users}, 200

    def post(self):
        user = create_user(request.get_json())
        return {'user': user}, 201


class UserProfile(Resource):
    def get(self, id):
        user = find_user(id)
        if user:
            return {'user': user}, 200
        return {'msg': 'Not found!'}, 404

    def put(self, id):
        user = find_user(id)
        if not user:
            return {'msg': 'Not found!'}, 404
        for key, value in request.get_json().items():
            if key in user.keys() and key != "id":
                user[key] = value
        return {'msg': f'User updated!'}, 200

    def delete(self, id):
        if delete_user(id):
            return {'msg': 'User deleted!'}, 200
        return {'msg': 'Not found!'}, 404


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

user_api = Api(user_bp)
user_api.add_resource(User, '/')
user_api.add_resource(UserProfile, '/<string:id>/')
