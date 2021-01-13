from twilio.rest import Client
import config

account_sid = config.TWILIO_ACCOUNT_SID
auth_token = config.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

message = 'Hello from Twilio API'
to = '+447952165272'
def TextAlert(message, to):
    message = client.messages \
                    .create(
                        body=message,
                        from_='+14343255105',
                        to=to
                    )

def setupCompleteSMS(to, to2, me, friend):
    message_user = "Hey "+str(me)+", you're all set up! We've let "+str(friend)+" know that you've joined 'U Okay Hun?'. We'll let you both know when you're listening to sadder music than usual."
    message_friend = "Hey "+str(friend)+", "+str(me)+" just joined 'U Okay Hun?'. They've asked us to let you know when they're listening to sadder music than usual." # SMS message to be send to the user
    TextAlert(message_user, to)
    TextAlert(message_friend, to2)

def simp_setupCompleteSMS(to, to2):
    message_user = "Hey, you're all set up! We've let your friend "+str(to2)+" know that you've joined 'U Okay Hun?'. We'll let you both know when you're listening to sadder music than usual."
    message_friend = "Hey, your friend "+str(to2)+" just joined 'U Okay Hun?'. They've asked us to let you know when they're listening to sadder music than usual." # SMS message to be send to the user
    TextAlert(message_user, to)
    TextAlert(message_friend, to2)

#setupCompleteSMS('+447952165272','+447758637203','Luke','Linda')
#simp_setupCompleteSMS('+447952165272','+447758637203')

if __name__ == "__main__":
    simp_setupCompleteSMS()
