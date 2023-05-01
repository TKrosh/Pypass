from flask import render_template, redirect
from flask import Flask, request
from forms import Password_generator, Authorization, Registration, Profile, AddInfo, ViewInfo, \
    ForgotPass, Create_new_password
from wtforms.validators import ValidationError
from work_func import create_password, empty_check, send_mail
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.user import User
from data.passwords import Passwords
import validators
from cryptography.fernet import Fernet
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'project_secret_key'
fernet = Fernet(b'o47K4w3jYCHsezSn_k2EAhnJGMpV8YKhWBmDzcsLNSA=')
pic_folder = os.path.join('data')
app.config['UPLOAD_FOLDER'] = pic_folder

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
@app.route('/')
def index():
    return render_template('index.html', title='Авторизация')

@app.route('/create_pass', methods=['GET', 'POST'])
def create_pass():
    error = ''
    res = ''
    form = Password_generator()
    if form.validate_on_submit():
        num = form.numbers.data
        s_letts = form.letters_small.data
        b_letts = form.letters_big.data
        sym = form.symbows.data
        long = form.password_length.data
        if any([num, s_letts, b_letts, sym]):
            res = create_password(num, s_letts, b_letts, sym, long)
        else:
            error = 'кажите из чего должен состоять пароль'
    return render_template('create_password.html', form=form, res=res, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Authorization()
    error = ''
    user_name = form.username.data
    db_sess = db_session.create_session()
    if form.forgot_pass.data:
        db_answear = db_sess.query(User.id).filter(User.name == user_name).first()
        if db_answear:
            return redirect(f'/new_pass/{db_answear[0]}')
        else:
            error = "Пользователь с таким логином не зарегистрирован"

    elif form.validate_on_submit():
        db_answear = db_sess.query(User).filter(User.name == user_name).first()
        if db_answear and db_answear.check_password(form.password.data):
            login_user(db_answear, remember=form.remember_me.data)
            return redirect('/')
        else:
            error = 'неверный логин или пароль'

    return render_template('Login.html', form=form, error=error)

@app.route('/new_pass/<int:id>', methods=['GET', 'POST'])
def new_pass(id):
    db_sess = db_session.create_session()
    error = ''
    mail = somedata = db_sess.query(User.email).filter(User.id == id).first()[0]
    encrypt_code = db_sess.query(User.reset_code).filter(User.id == id).first()[0]
    if encrypt_code:
        code_sended = True
    else:
        code_sended = False
    form = ForgotPass()
    if form.send_code.data:
        code_sended = True
        code = create_password(1, 0, 1, 0, 6)
        somedata = db_sess.query(User).filter(User.id == id).first()
        somedata.reset_code = fernet.encrypt(code.encode())
        db_sess.commit()
        send_mail(code, mail, 'Код востановления пароля')
    elif form.reset.data and form.code_field.data:
        encrypt_code = db_sess.query(User.reset_code).filter(User.id == id).first()[0]
        code = fernet.decrypt(encrypt_code).decode()
        if form.code_field.data == code and code:
            somedata = db_sess.query(User).filter(User.id == id).first()
            somedata.reset_code = ''
            db_sess.commit()
            return redirect(f'/reset_pass/{id}')
        else:
            error = 'Неверный код'
    return render_template('new_pass.html', title='Авторизация', form=form, code_sended=code_sended,
                           mail=mail, error=error)

@app.route('/reset_pass/<int:id>', methods=['GET', 'POST'])
def reset_pass(id):
    form = Create_new_password()
    error = ''
    if form.validate_on_submit():
        if form.new_pass.data != form.rep_new_pass.data:
            error = 'пароли не совпадают'
        else:
            user = User()
            db_sess = db_session.create_session()
            somedata = db_sess.query(User).filter(User.id == id).first()
            somedata.password = user.set_password(form.new_pass.data)
            db_sess.commit()
            return redirect('/')
    return render_template('new_password.html', form=form, error=error)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = Profile()
    if form.validate_on_submit():
        logout_user()
        return redirect('/')
    return render_template('profile.html', form=form)

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    form = Registration()
    error = ''
    if form.validate_on_submit():
        if form.password.data != form.repied_password.data:
            error = 'пароли не совпадают'
        else:
            user = User(
                name=form.username.data,
                email=form.mail.data
            )
            db_sess = db_session.create_session()
            user.password = user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
    return render_template('regist.html', form=form, error=error)

@app.route('/View_list', methods=['GET', 'POST'])
def View_list():
    form = ViewInfo()
    db_sess = db_session.create_session()
    password = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id)
    if form.validate_on_submit():
        text = form.search_field.data
        password = list(db_sess.query(Passwords).filter((Passwords.user_id == current_user.id),
                                                        (Passwords.title.like(f'%{text.lower()}%')) |
                                                        (Passwords.title.like(f'%{text.upper()}%'))))
    empty_list = empty_check(list(password))
    return render_template('View_list.html', password=password, form=form, title='!!!!', empty_list=empty_list)

@app.route('/View_list_withinfo/<int:id>', methods=['GET', 'POST'])
def View_list_withinfo(id):
    form = ViewInfo()
    db_sess = db_session.create_session()
    password = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id)
    show_info = db_sess.query(Passwords).filter(Passwords.id == id).first()
    show_pass = fernet.decrypt(show_info.password).decode()
    if form.validate_on_submit():
        text = form.search_field.data
        password = list(db_sess.query(Passwords).filter((Passwords.user_id == current_user.id),
                                                        (Passwords.title.like(f'%{text.lower()}%')) |
                                                        (Passwords.title.like(f'%{text.upper()}%'))))
    empty_list = empty_check(list(password))
    return render_template('View_list.html', password=password, form=form, title='!!!!',
                           show_info=show_info, empty_list=empty_list, show_pass=show_pass)


@app.route('/delete_info/<int:id>', methods=['GET', 'POST'])
def delete_info(id):
    form = ViewInfo()
    db_sess = db_session.create_session()
    db_sess.query(Passwords).filter(Passwords.id == id).delete()
    db_sess.commit()
    password = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id)
    show_info = db_sess.query(Passwords).filter(Passwords.id == id).first()
    if form.validate_on_submit():
        text = form.search_field.data
        password = list(db_sess.query(Passwords).filter((Passwords.user_id == current_user.id),
                                                        (Passwords.title.like(f'%{text.lower()}%')) |
                                                        (Passwords.title.like(f'%{text.upper()}%'))))
    empty_list = empty_check(list(password))
    return render_template('View_list.html', password=password, form=form, title='!!!!',
                           show_info=show_info, empty_list=empty_list)


@app.route('/change_info/<int:id>', methods=['GET', 'POST'])
def change_info(id):
    error = ''
    form = AddInfo()
    db_sess = db_session.create_session()
    #взять нужную запись
    somedata = db_sess.query(Passwords).filter(Passwords.id == id).first()
    #поместить информацию в строки
    form.title.data = somedata.title
    form.login.data = somedata.login
    form.password.data = fernet.decrypt(somedata.password).decode()
    form.site.data = somedata.site
    form.note.data = somedata.note
    if form.validate_on_submit():
        link = request.form.get('site')
        if not validators.url(link) and link:
            error = "Укажите настоящую ссылку на сайт"
        else:
            #изменяем данные (запрос задаётся через get, потому что по другому не работает)
            somedata.title = request.form.get('title')
            somedata.login = request.form.get('login')
            somedata.password = fernet.encrypt(request.form.get('password').encode())
            somedata.site = link
            somedata.note = request.form.get('note')
            db_sess.commit()
            return redirect('/View_list')
    return render_template('adding.html', form=form, error=error)


@app.route('/Adding_info', methods=['GET', 'POST'])
def Adding_info():
    form = AddInfo()
    if form.validate_on_submit():
        addinfo = Passwords(
            title = form.title.data,
            login = form.login.data,
            user_id = current_user.id,
            password = fernet.encrypt(form.password.data.encode()),
            site = form.site.data,
            note = form.note.data
        )
        db_sess = db_session.create_session()
        db_sess.add(addinfo)
        db_sess.commit()
        return redirect('/View_list')
    return render_template('adding.html', form=form)

if __name__ == '__main__':
    db_session.global_init("db/passwords.db")

    app.run(port=8080, host='127.0.0.1')
