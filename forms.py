from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Optional, Length
from validators import UniqueUsername, UniqueUsermail, InetegerRequired, SpaceRequired

class Password_generator(FlaskForm):
    result_box = StringField()
    numbers = BooleanField('Использовать цифры')
    letters_small = BooleanField('Использовать строчны букви (Латинские)')
    letters_big = BooleanField('Использовать заглавные букви (Латинские)')
    symbows = BooleanField('Использовать спец. символы (!?#$%)')
    password_length = StringField('Длина пароля', validators=[DataRequired(), InetegerRequired])
    create = SubmitField('Сгенерировать')


class Authorization(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = StringField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('запомнить меня')
    submit = SubmitField('войти')


class Registration(FlaskForm):
    username = StringField('Логин:  ', validators=[DataRequired(), UniqueUsername])
    mail = StringField('почта:  ', validators=[DataRequired(), UniqueUsermail])
    password = StringField('Пароль:  ', validators=[DataRequired()])
    repied_password = StringField('Повторите пароль:  ', validators=[DataRequired()])
    submit = SubmitField('зарегистрироваться')


class Profile(FlaskForm):
    quit = SubmitField('Выйти')


class AddInfo(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=30)])
    login = StringField('Логин', validators=[DataRequired(), Length(max=40)])
    password = StringField('пароль', validators=[DataRequired(), Length(max=40)])
    note = StringField('Заметки', validators=[SpaceRequired])
    site = StringField('Ссылка на сайт (не обязательно)')
    submit = SubmitField('Сохранить')


class ViewInfo(FlaskForm):
    search_field = StringField(validators=[DataRequired()])
    search = SubmitField('поиск')
    show_info_button = SubmitField('просмотр')