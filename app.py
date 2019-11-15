from fantasybooks_api import create_app, db
from fantasybooks_api.models import AuthorModel, BookModel, UserModel

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Users=UserModel, Authors=AuthorModel, Books=BookModel)


if __name__ == '__main__':
    app.run()
