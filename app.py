from flask import Flask, render_template, request, flash, session
from flask import redirect, url_for, make_response
import twilio.twiml

from functools import wraps

from utils.forms import *
from utils import api, outbound_messages
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

"""
Home page
"""
@app.route('/')
def home():
    return render_template('home.html')

"""
User functionality
TODO: Move in to views/users.py file
"""
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
            return redirect(url_for('login'))

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
            response = make_response(redirect(url_for('user_page')))
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
def user_page():
    user = api.get_user_info(request)
    groups = api.get_user_groups(user['userName'], request.cookies) # TODO: Make User model that is built from dict
    return render_template('users/home.html', user=user, groups=groups)

"""
Groups functionality
TODO: Move in to views/groups.py file
"""

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'GET':
        form = GroupForm(request.form)
        return render_template('forms/group.html', form=form)
    else:
        success, error = api.create_group(request.form, request.cookies)
        if not success:
            flash(error['Message'])
            form = GroupForm(request.form)
            return render_template('forms/group.html', form=form)
        else:
            flash('New group successfully created!')
            group_name = request.form['Name']
            outbound_messages.send_group_created_notification(group_name)
            url = '/groups/{group}'.format(group=group_name)
            return redirect(url)

@app.route('/groups/<group_name>', methods=['GET'])
def group_page(group_name):
    group = api.get_group_info(group_name)
    users = api.get_group_users(group_name)
    return render_template('groups/home.html', group=group, users=users)

"""
Texts endpoint
"""
@app.route('/texts', methods=['GET', 'POST'])
def receive_message():
    """ Receive and parse incoming group messages """

    sender_number = request.values.get('From', None)
    receiving_number = request.values.get('To', None)
    message_body = request.values.get('Body', '')

    # TODO: Add security so only group members can send texts to the group
    sending_user = api.get_user_from_number(sender_number)
    receiving_group = api.get_group_from_number(receiving_number)

    # Just send response for now, but later send to all group members + don't
    # reply to original sender
    forwarded_message = ': '.join([sending_user['firstName'], message_body])
    resp = twilio.twiml.Response()
    resp.message(forwarded_message)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
