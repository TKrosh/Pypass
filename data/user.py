import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reset_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"'id': {self.id}, 'name': {self.name}, 'email':{self.email}, 'password': {self.password}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        return self.hashed_password

    def check_password(self, password):
        return check_password_hash(self.password, password)