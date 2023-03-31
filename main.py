from flask import render_template
from flask import Flask
from forms import Password_generator
import os
print("!!")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'project_secret_key'

pic_folder = os.path.join('data')
app.config['UPLOAD_FOLDER'] = pic_folder


@app.route('/')
def index():

    p = 'static/data/key.png'
    form = Password_generator()
    if form.validate_on_submit():
        print('!!!!!')
    return render_template('index.html', title='Авторизация', form=form, png_link=p)

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/View_list')
def View_list():
    return render_template('View_list.html')

@app.route('/Adding_info')
def Adding_info():
    return render_template('adding.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')