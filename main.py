from flask import render_template, redirect
from flask import Flask
from forms import Password_generator, Authorization, Registration
from wtforms.validators import ValidationError
from work_func import create_password
from data import db_session
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'project_secret_key'

pic_folder = os.path.join('data')
app.config['UPLOAD_FOLDER'] = pic_folder


@app.route('/')
def index():
    p = 'static/data/key.png'
    return render_template('index.html', title='Авторизация')

@app.route('/create_pass', methods=['GET', 'POST'])
def create_pass():
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
    return render_template('create_password.html', form=form, res=res)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Authorization()
    return render_template('Login.html', form=form)


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    form = Registration()
    if form.validate_on_submit():
        print(form.username.data)
        return redirect('/')
    return render_template('regist.html', form=form)

@app.route('/View_list')
def View_list():
    return render_template('View_list.html')

@app.route('/Adding_info')
def Adding_info():
    return render_template('adding.html')

if __name__ == '__main__':
    db_session.global_init("db/passwords.db")
    app.run(port=8080, host='127.0.0.1')