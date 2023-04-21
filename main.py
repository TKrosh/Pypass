from flask import render_template, redirect
from flask import Flask
from forms import Password_generator, Authorization, Registration, Profile, AddInfo
from wtforms.validators import ValidationError
from work_func import create_password, get_user_id
from data import db_session
from data.user import User
from data.passwords import Passwords
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'project_secret_key'

pic_folder = os.path.join('data')
app.config['UPLOAD_FOLDER'] = pic_folder
Authorizated = 0
username, user_id = 'login', 0

@app.route('/')
def index():
    return render_template('index.html', title='Авторизация', Authorizated=Authorizated, username=username)

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
    return render_template('create_password.html', form=form, res=res, Authorizated=Authorizated, username=username, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global Authorizated, username, user_id
    form = Authorization()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_answear = list(db_sess.query(User).filter((User.name == form.username.data) and
                                                    (User.password == form.password.data)))
        if db_answear:
            Authorizated = 1
            username = form.username.data
            user_id = get_user_id(form.username.data, form.password.data)
            return redirect('/')
    return render_template('Login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global Authorizated, username
    form = Profile()
    if form.validate_on_submit():
        Authorizated = 0
        return redirect('/')
    return render_template('profile.html', form=form, Authorizated=Authorizated, username=username)

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    global Authorizated, username
    form = Registration()
    error = ''
    if form.validate_on_submit():
        user = User()
        user.name = form.username.data
        user.email = form.mail.data
        user.password = form.password.data
        if form.password.data != form.repied_password.data:
            error = 'пароли не совпадают'
        else:
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            Authorizated = 1
            username = form.username.data
            return redirect('/')
    return render_template('regist.html', form=form, error=error)

@app.route('/View_list', methods=['GET', 'POST'])
def View_list():
    db_sess = db_session.create_session()
    print(user_id)
    password = db_sess.query(Passwords).filter(Passwords.user_id == user_id)
    return render_template('View_list.html', Authorizated=Authorizated,
                           username=username, password=password)

@app.route('/Adding_info', methods=['GET', 'POST'])
def Adding_info():
    form = AddInfo()
    if form.validate_on_submit() and user_id:
        addinfo = Passwords()
        addinfo.title = form.title.data
        addinfo.login = form.login.data
        addinfo.user_id = user_id
        addinfo.password = form.password.data
        addinfo.site = form.site.data
        addinfo.note = form.note.data
        db_sess = db_session.create_session()
        db_sess.add(addinfo)
        db_sess.commit()
        return redirect('/View_list')
    return render_template('adding.html', form=form, Authorizated=Authorizated, username=username)

if __name__ == '__main__':
    db_session.global_init("db/passwords.db")
    app.run(port=8080, host='127.0.0.1')
