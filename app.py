from fantasybooks_api import create_app, db
from fantasybooks_api.models import UserModel

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=UserModel)


if __name__ == '__main__':
    app.run()
