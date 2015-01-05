"""
Functions for sending text messages from the server
to group members
"""

from twilio.rest import TwilioRestClient
import requests

import api
import settings
import secrets # TODO: Configure this to get API auth stuff from env variables

client = TwilioRestClient(secrets.TWILIO_SID, secrets.TWILIO_AUTH_TOKEN)

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
