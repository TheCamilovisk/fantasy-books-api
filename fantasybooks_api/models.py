from fantasybooks_api import db, bcrypt
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import SQLAlchemyError


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=True, default=None)
    surname = db.Column(db.String(120), nullable=True, default=None)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(
        self,
        username,
        password,
        email,
        name=None,
        surname=None,
        created_at=None,
        updated_at=None,
        last_activity=None,
        is_admin=False,
    ):
        super().__init__()
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_activity = last_activity
        self.is_admin = is_admin

        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete(cls, id):
        user = cls.get(id)
        if not user:
            raise RuntimeError('User does not exists')

        db.session.delete(user)
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error
