from wtforms.validators import DataRequired, ValidationError
from data import db_session
from data.user import User
from flask import Flask, request

def InetegerRequired(form, password_length):
    if not form.password_length.data.isdigit():
        raise ValidationError("Не верное значение длины пароля")


def UniqueUsername(form, username):
    db_sess = db_session.create_session()
    db_answear = list(db_sess.query(User).filter(User.name == form.username.data))
    print(db_answear)
    if db_answear:
        raise ValidationError("Это имя пользователя уже занято")

def UniqueUsermail(form, mail):
    db_sess = db_session.create_session()
    db_answear = list(db_sess.query(User).filter(User.name == form.mail.data))
    if db_answear:
        raise ValidationError("Это почта уже занята")

def SpaceRequired(form, note):
    #эта функция нужнав чтобы текст помещался на странице при просмотре
    letters_amount = len(request.form.get('note'))
    space_count = request.form.get('note').count(' ') + 1
    print(space_count)
    if letters_amount // space_count > 35:
        raise ValidationError("слишком мало пробелов(это вызовет проблемы с чтение записи, каждые 35 символов)")

def AsymRequired(form, mail):
    if '@' not in form.mail.data:
        raise ValidationError("Электронная почта должна включать в себя символ '@'")

