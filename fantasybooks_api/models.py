from fantasybooks_api import db, bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(
        self,
        username,
        password,
        name,
        surname,
        email,
        created_at=None,
        updated_at=None,
        last_activity=None,
    ):
        super().__init__()
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_activity = last_activity

        self.set_password(password)

    def set_password(self, plaintext):
        self.password = bcrypt.generate_password_hash(plaintext)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error

    def update(self, **kwargs):
        for key, value in kwargs['data'].items():
            if key in self.__dict__:
                self.__setattr__(key, value)

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error

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
