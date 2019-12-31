# https://github.com/TwilioDevEd/sdk-starter-python

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import os
from flask import Flask, jsonify, request
from response_logic import generate_response
from faker import Faker
from twilio.rest import Client
# from twilio.jwt.access_token import AccessToken
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.jwt.access_token.grants import (
#     SyncGrant,
#     VideoGrant,
#     ChatGrant
# )
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname
from inflection import underscore

import dialogflow

sentry_sdk.init(
    dsn="https://c26911992b3a40beb9afc2aaa749ab83@sentry.io/1867953",
    integrations=[FlaskIntegration()]
)

TWILIO_NUMBER = "+18313161352"

# Convert keys to snake_case to conform with the twilio-python api definition contract
def snake_case_keys(somedict):
    snake_case_dict = {}
    for key, value in somedict.items():
        snake_case_dict[underscore(key)] = value
    return snake_case_dict

app = Flask(__name__)
# fake = Faker()

#use this to set environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@app.route('/')
def index():
    return "OK"

@app.route('/inbound_sms', methods=['POST'])
def inbound_sms():
    message = request.form['Body']
    phone_number = request.form['From']
    response = generate_response(phone=phone_number, message=message)
    return str(response)

# Ensure that the Sync Default Service is provisioned
def provision_sync_default_service():
    client = Client(os.environ['TWILIO_API_KEY'], os.environ['TWILIO_API_SECRET'], os.environ['TWILIO_ACCOUNT_SID'])
    client.sync.services('default').fetch()

if __name__ == '__main__':
    provision_sync_default_service()
    app.run(debug=True, host='0.0.0.0')
