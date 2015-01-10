import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('MODE') == 'DEV':
    # Enable debug mode. Turn off in production.
    DEBUG = True
else:
    DEBUG = False

SECRET_KEY = 'something super secret'
