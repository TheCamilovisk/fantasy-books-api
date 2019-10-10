import click
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError
from getpass import getpass

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
    password1 = getpass('Enter your password: ')
    password2 = getpass('Re-enter your password: ')
    if password1 != password2:
        print('Password do not match')
        return

    superuser = User(username, password1, name, surname, email)
    superuser.save()

    print('Super user created.')
