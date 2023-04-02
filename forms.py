from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def InetegerRequired(form, password_length):
    if not form.password_length.data.isdigit():
        raise ValidationError("Не верное значение длины пароля")

def MaterialRequired(form, numbers, letters_small, letters_big, symbows):
    num = form.numbers.data
    s_letts = form.letters_small.data
    b_letts = form.letters_big.data
    sym = form.symbows.data
    if not any([num, s_letts, b_letts, sym]):
        raise ValidationError("Укажите из чего должен состоять пароль")

class Password_generator(FlaskForm):
    result_box = StringField()
    numbers = BooleanField('Использовать цифры')
    letters_small = BooleanField('Использовать строчны букви (Латинские)')
    letters_big = BooleanField('Использовать прописные букви (Латинские)')
    symbows = BooleanField('Использовать спец. символы (!?#$%)')
    password_length = StringField('Длина пароля', validators=[DataRequired(), InetegerRequired])
    create = SubmitField('Сгенерировать')

    def material_req(self):
        raise ValidationError("Укажите из чего должен состоять пароль")


class Authorization(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = StringField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('запомнить меня')
    submit = SubmitField('войти')


class Registration(FlaskForm):
    username = StringField('Логин:  ', validators=[DataRequired()])
    mail = StringField('почта:  ', validators=[DataRequired()])
    password = StringField('Пароль:  ', validators=[DataRequired()])
    repied_password = StringField('Повторите пароль:  ', validators=[DataRequired()])
    submit = SubmitField('зарегистрироваться')