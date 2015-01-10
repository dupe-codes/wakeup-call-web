"""
Settings specific to the functionality of app utilities
"""

import os

if os.environ.get('MODE') == 'DEV':
    BACKEND_URL = 'http://localhost:8080'
else:
    BACKEND_URL = 'https://wakeup-backend.herokuapp.com'
