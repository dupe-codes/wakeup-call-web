"""
Functions for sending text messages from the server
to group members
"""

import os
import requests
from twilio.rest import TwilioRestClient

import api
import settings

try:
    from secrets import *
except ImportError:
    TWILIO_SID = os.environ.get('TWILIO_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_group_created_notification(group_name):
    """ Sends a text confirmation that group has been created """
    group_info = api.get_group_info(group_name)
    group_number = group_info['phoneNumber']
    message = 'Congratulations, your group {group_name} has successfully been created. Save this number!'.format(
        group_name=group_name
    )

    group_users = api.get_group_users(group_name)
    for user in group_users:
        user_number = user['phoneNumber']
        client.messages.create(
            from_=group_number,
            to=user_number,
            body=message,
        )

def send_invite_message(user_data, group, invite_code):
    """ Sends a text message invite to a new user to join the given group """
    return
