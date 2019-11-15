from datetime import datetime
from hashlib import md5

from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from fantasybooks_api import bcrypt, db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('model', '') + 's'

    def save(self):
        db.session.add(self)
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
            raise RuntimeError('Not found')

        db.session.delete(user)
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error


class UserModel(BaseModel):
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=True, default=None)
    surname = db.Column(db.String(120), nullable=True, default=None)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.last_activity = last_activity
        self.is_admin = is_admin

        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    @classmethod
    def find(cls, username):
        return cls.query.filter_by(username=username).first()

    def avatar(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'http://www.gravatar.com/avatar/{digest}?d=identicon'


class AuthorModel(BaseModel):
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    books = db.relationship('BookModel', backref='author', lazy=True)

    @classmethod
    def find(cls, name):
        name = name.lower()
        return cls.query.filter(
            or_(
                func.lower(cls.name).contains(name),
                func.lower(cls.surname).contains(name),
            )
        ).all()


class BookModel(BaseModel):
    title = db.Column(db.String(300), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    @classmethod
    def find(cls, name):
        return cls.query.filter(func.lower(cls.title).contains(name.lower())).all()
