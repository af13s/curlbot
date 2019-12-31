from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
import os

acct_sid = "AC5679fe7e61f28f6c925d3893591831d0"
auth_token = "59290cc8c570abae3776c06168ea79a3"

TWILIO_NUMBER = "+18313161352"
TEST_PHONE = "+19543984645"

class TwilioClient:

    def __init__(self):
        self.client = Client(acct_sid, auth_token)
    
    def outbound_sms(self, message, recipient_phone):

        response = self.client.messages.create(
            to = recipient_phone,
            from_=TWILIO_NUMBER,
            body=message
        )

        # print(response)
        # return response
