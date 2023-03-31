from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Password_generator(FlaskForm):
    result_box = StringField(validators=[DataRequired()])
    numbers = BooleanField('Добавить цифры')
    letters_small = BooleanField('Добовить строчны букви (Латинские)')
    letters_big = BooleanField('Добовить прописные букви (Латинские)')
    symbows = BooleanField('Запомнить меня')
    create = SubmitField('Сгенерировать')