from flask import Blueprint, request
from flask_restful import Resource, Api


mock_users = [
    {
        'id': 0,
        'username': 'username0',
        'name': 'User',
        'surname': '0',
        'email': 'user0@example.com',
        'created_at': '2019-08-06 20:54:47.051355',
        'updated_at': '2019-08-16 20:54:47.051355',
        'last_activity': '2019-08-17 20:54:47.051355',
    },
    {
        'id': 1,
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
    user_dict['id'] = len(mock_users)
    mock_users.append(user_dict)
    return mock_users[-1]


class User(Resource):
    def get(self):
        return {'users': mock_users}

    def post(self):
        user = create_user(request.get_json())
        return {'user': user}


class UserProfile(Resource):
    def get(self, id):
        return {'user': mock_users[id]}

    def put(self, id):
        return {'msg': f'Update user id: {id}'}

    def delete(self, id):
        return {'msg': f'Delete user id: {id}'}


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

user_api = Api(user_bp)
user_api.add_resource(User, '/')
user_api.add_resource(UserProfile, '/<int:id>/')
