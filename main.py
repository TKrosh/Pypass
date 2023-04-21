from flask import render_template, redirect
from flask import Flask
from forms import Password_generator, Authorization, Registration, Profile, AddInfo, ViewInfo
from wtforms.validators import ValidationError
from work_func import create_password, get_user_id
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.user import User
from data.passwords import Passwords
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'project_secret_key'

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
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_answear = db_sess.query(User).filter(User.name == form.username.data).first()
        if db_answear and db_answear.check_password(form.password.data):
            login_user(db_answear, remember=form.remember_me.data)
            return redirect('/')
        else:
            error = 'неверный логин или пароль'
    return render_template('Login.html', form=form, error=error)

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
            return redirect('/')
    return render_template('regist.html', form=form, error=error)

@app.route('/View_list', methods=['GET', 'POST'])
def View_list():
    form = ViewInfo()
    db_sess = db_session.create_session()
    password = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id)
    if form.validate_on_submit():
        pass
    return render_template('View_list.html', password=password, form=form, title='!!!!')

@app.route('/View_list_withinfo/<int:id>', methods=['GET', 'POST'])
def View_list_withinfo(id):
    form = ViewInfo()
    db_sess = db_session.create_session()
    password = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id)
    show_info = db_sess.query(Passwords).filter(Passwords.id == id).first()
    if form.validate_on_submit():
        pass
    return render_template('View_list.html', password=password, form=form, title='!!!!', show_info=show_info)


@app.route('/Adding_info', methods=['GET', 'POST'])
def Adding_info():
    form = AddInfo()
    if form.validate_on_submit():
        addinfo = Passwords(
            title = form.title.data,
            login = form.login.data,
            user_id = current_user.id,
            password = form.password.data,
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
