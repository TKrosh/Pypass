import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Passwords(SqlAlchemyBase):
    __tablename__ = 'password'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    site = sqlalchemy.Column(sqlalchemy.String)
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def __repr__(self):
        return f'{self.title};{self.login};'