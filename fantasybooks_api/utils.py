import click
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from fantasybooks_api.models import User


def handle_sqlalchemy_error(error: SQLAlchemyError) -> str:
    return str(error.__dict__['orig'])


@click.command('createsuperuser')
@click.argument('username')
@click.argument('email')
@click.argument('name')
@click.argument('surname')
@with_appcontext
def createsuperuser(username, email, name, surname):
    password = input('Enter your password: ')
    if input('Re-enter your password: ') is not password:
        print('Password do not match')

    superuser = User(username, password, name, surname, email)
    superuser.save()

    print('Super user created.')
