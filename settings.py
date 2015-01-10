import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('MODE') == 'PROD':
    DEBUG = False
    PORT = os.environ.get('PORT')
else:
    DEBUG = True
    PORT = 5000

SECRET_KEY = 'something super secret'
