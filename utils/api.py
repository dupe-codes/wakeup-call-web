"""
This file contains definitions of several functions for interacting
with the wakeup call backend
"""

import requests

import settings

def registerNewUser(params):
    """
    Forwards registration request to the API backend

    Returns True on registration success, False on failure.
    """
    response = requests.post(settings.BACKEND_URL + '/users', params=params)
    print response.json()
    return True

def loginUser(params):
    response = requests.post(settings.BACKEND_URL + '/users/login', params=params)
    print response.headers
    return True
