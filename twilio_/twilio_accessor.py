from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
import os

acct_sid = os.environ["ACCT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

TWILIO_NUMBER = "+18313161352"
TEST_PHONE = "+19543984645"

class TwilioClient:

    def __init__(self):
        self.client = Client(acct_sid, auth_token)
    
    def outbound_sms(self, message, recipient_phone):

        response = self.client.messages.create(
            # to=recipient_phone,
            to = TEST_PHONE,
            from_=TWILIO_NUMBER,
            body=message
        )

        print(response)
        # return response
