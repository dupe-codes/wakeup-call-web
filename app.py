from flask import Flask, render_template, request, flash, session
from flask import redirect, url_for, make_response

from functools import wraps

from utils.forms import *
from utils import api
import settings

app = Flask(__name__)
app.config.from_object('settings')

def login_required(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        if 'wakeup-session' not in request.cookies:
            flash('You must be logged in to view this page')
            return redirect(url_for('login'))
        else:
            if not api.verify_cookie(request.cookies['wakeup-session']):
                flash('You must be logged in to view this page')
                return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrap

@app.route('/test')
@login_required
def test():
    return render_template('home.html')

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
        if not outcome['success']:
            error_msg = outcome['error']['Message']
            flash(error_msg)
            form = RegisterForm(request.form)
            return render_template('forms/register.html', form=form)
        else:
            flash('Successfully registered, you may now login!')
            form = LoginForm(request.form)
            return render_template('forms/login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)
    else:
        outcome = api.loginUser(request.form)
        if not outcome['success']:
            error_msg = outcome['error']['Message']
            flash(error_msg)
            form = LoginForm(request.form)
            return render_template('forms/login.html', form=form)
        else:
            flash('Successfully logged in!')
            response = make_response(redirect(url_for('test')))
            response.headers['Set-Cookie'] = outcome['cookie']
            return response

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('home')))

    # Delete any current sessions by overwriting cookie w/ expired one
    response.set_cookie('wakeup-session', '', expires=0)
    return response

@app.route('/users/home', methods=['GET'])
@login_required
def userPage():
    user_info = api.get_user_info(request)
    groups = api.get_user_groups(user_info)
    return render_template('users/home.html', user=user_info, groups=groups)

if __name__ == '__main__':
    app.run(debug=True)
