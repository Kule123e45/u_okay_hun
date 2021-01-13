import os
from twilio.rest import Client
import config
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config.TWILIO_ACCOUNT_SID
auth_token = config.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

def TextAlert(message, to):
    message = client.messages \
                    .create(
                        body=message,
                        from_='+14343255105',
                        to=to
                    )
message = "U okay hun? It looks like you're listening to some sad music, maybe switch it up a bit?"
to = '+447952165272'

TextAlert(message, to)
