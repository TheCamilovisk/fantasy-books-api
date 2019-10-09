from sqlalchemy.exc import SQLAlchemyError


def handle_sqlalchemy_error(error: SQLAlchemyError) -> str:
    return str(error.__dict__['orig'])
