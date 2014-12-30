from flask import Flask, render_template, request

from utils.forms import *
from utils import api
import settings

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(request.form)
        return render_template('forms/register.html', form=form)
    else:
        outcome = api.registerNewUser(request.form)
        return 'Done'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)
    else:
        outcome = api.loginUser(request.form)
        return 'Done'

if __name__ == '__main__':
    app.run(debug=True)
