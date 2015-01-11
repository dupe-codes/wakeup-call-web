"""
Settings specific to the functionality of app utilities
"""

import os

if os.environ.get('MODE') == 'PROD':
    BACKEND_URL = 'https://wakeup-backend.herokuapp.com'
else:
    BACKEND_URL = 'http://localhost:8080'
