from dialogflow.dialogflow_accessor import DialogFlowClient
from database.database_accessor import database
from twilio_.twilio_accessor import TwilioClient
from ingredients_repo import (
   ALCOHOL_INFO,
   ALCOHOL_DICT,
   SULFATE_INFO,
   SULFATE_DICT,
   PSW_INFO,
   PSW_DICT,
   WAX_INFO,
   WAX_DICT
)
import os
from datetime import datetime
from time import sleep


AWS_ACCESS_KEY_ID =os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION_NAME='us-west-1'


PRODUCT_LOOKUP = "Product Lookup"
HAIR_RECOMMENDATION = "Hair Recommendation"

PRODUCT_TABLE = "product"
PRODUCT_SEARCH_TABLE = "searches"
MESSAGE_TABLE = "messages"
   
def get_product_ingredients(key_var,range_var):
   
   client = database.dynambo_admin_client()
   response = client.get_item(
    TableName=PRODUCT_TABLE,
    Key={
       "product_name": {'S': key_var},
       "brand_name": {'S': range_var }
   },
    AttributesToGet=[
        "ingredients",
    ])

   return response["Item"]["ingredients"]["S"]

def get_datetime_epoch():
   epoch = int(datetime.now().timestamp())
   return epoch

def get_datetime():
   return str(datetime.now())

def record_message(message, phone_number):

   item = {
      "user_phone": phone_number,
      "datetime": get_datetime(),
      "message": message,
      "datetime_epoch": get_datetime_epoch()
   }
   
   database.add_table_entry(MESSAGE_TABLE, item)

def record_product_search(phone_number, product_name, brand_name):
   item = {
      "user_phone": phone_number,
      "datetime": get_datetime(),
      "product_name": product_name,
      "brand_name": brand_name,
      "datetime_epoch": get_datetime_epoch()
   }

   database.add_table_entry(PRODUCT_SEARCH_TABLE, item)

def record_user_info(phone_number, curl_type, **kwargs):
   item = {
      "user_phone": phone_number,
      "curl_type": curl_type,
   }

   for key, value in kwargs.items():
      item[key] = value
   
   database.add_table_entry(tablename, item)


def ingredients_analyzer(ingredients_string):

   ingredients_list = ingredients_string.split(",")
   ingredients_list = [ingredient.strip() for ingredient in ingredients_list]

   ingredients_set = set(ingredients_list)

   ingred_infos = [
      ALCOHOL_INFO,
      SULFATE_INFO,
      PSW_INFO,
      WAX_INFO
   ]

   ingred_dicts = [
      ALCOHOL_DICT,
      SULFATE_DICT,
      PSW_DICT,
      WAX_DICT
   ]

   report = []

   for x in range (len(ingred_dicts)):
      detected = {}
      for key,values in ingred_dicts[x].items():
         for value in values:
            if value in ingredients_set:
               if key not in detected:
                  detected[key] = []
               detected[key].append(value)
      for key in detected:
         msg = ingred_infos[x][key] + " [" + ", ".join(detected[key]) + "]"
         report.append(msg)

   return "\n\n".join(report)


def generate_response(phone, message):

   record_message(message=message,phone_number=phone)
   agent = DialogFlowClient(phone)
   twilio_client = TwilioClient()

   reply = ""
   intent, variables, reply = agent.analyze_msg(message)

   twilio_client.outbound_sms(reply,phone)
   sleep(5)

   

   if intent == PRODUCT_LOOKUP:

      ## TODO ##
      # if multiple values returned then ask user which one to go with

      try:
         hair_company = variables["HairCompany"].values[0].string_value
      except Exception as e:
         msg = "Try again and include the company"
         twilio_client.outbound_sms(msg, phone)
         return

      try:
         product_name = variables[hair_company.replace(" ", "").lower()+"product"].values[0].string_value
      except Exception as e:
         msg = "product couldnt be found :("
         twilio_client.outbound_sms(msg, phone)
         return

      record_product_search(phone_number=phone, product_name=product_name, brand_name=hair_company)

      # print(hair_company, ":", product_name)
      ingredients = get_product_ingredients(key_var=product_name, range_var=hair_company)

      ingredients_message = "{} Ingredients: {}".format(product_name, ingredients)

      if ingredients:
         twilio_client.outbound_sms(ingredients_message, phone)
         reply = ingredients_analyzer(ingredients)
         twilio_client.outbound_sms(reply, phone)
      else:
         msg = "Ingredients haven't been found :("
         twilio_client.outbound_sms(msg, phone)
         return

   # if intent == HAIR_RECOMMENDATION:
   #    try: 
   #       record_user_info(phone_number, curl_type, ...)
   #    except Exception as e:
   #       print("Error occured trying to add new entry %s", s)

   #    recommendation = dataset_search(hair_type=variables["hair_type"])
   #    reply = recommendation


   
   # string = "Hello from twilio\n "
   # string += message

   # return reply

# INGREDIENT_TEST_STRING = "wax, cire, cera, paraffin,ammonium lauryl sulfate, ammonium lauryl sulphate, aqua water eau, glycerin , xanthan gum, betaine, argania spinosa kernel oil , mauritia flexuosa fruit oil , cucurbita pepo pumpkin seed oil , aloe barbadensis leaf juice , pectin, helianthus annuus sunflower seed oil , rosmarinus officinalis rosemary leaf extract , citrus aurantium dulcis orange peel oil , citrus grandis grapefruit peel oil , citrus limon lemon peel oil , alcohol , cucumis sativus cucumber fruit extract , vanilla planifolia fruit extract , potassium sorbate, chenopodium quinoa seed extract , chamomilla recutita matricaria flower extract , calendula officinalis flower extract , limonene , sodium benzoate, fragrance parfum"

# while (True):
#    string = input(">: ")
#    if string == "exit":
#       break
   
#    # print(generate_response("+19543984645", string))
#    # print(ingredients_analyzer(INGREDIENT_TEST_STRING))
   



####

### TODO ### 

# Store all user messages in the database and timestamp the messages

# schema phone_number: string
#        message: string
#        datetime: string
#        epoch_timestamp: number

# train dialogflow to understand the messages - take the names in the database and create permutations for dialogflow to train on

# take a message
# extract the variables - use dialogflow to recognize the entities
# discover the intent - sending the message to dialog flow
# response based on intent - add fulfillment webhook to the product. get the intent and use that to form the logic


# put logic for responsing a database so that we can update and reference it
# make adding new commands extensible




# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# @app.route('/video/')
# def video():
#     return app.send_static_file('video/index.html')

# @app.route('/sync/')
# def sync():
#     return app.send_static_file('sync/index.html')

# @app.route('/notify/')
# def notify():
#     return app.send_static_file('notify/index.html')

# @app.route('/chat/')
# def chat():
#     return app.send_static_file('chat/index.html')



# # Basic health check - check environment variables have been configured
# # correctly
# @app.route('/config')
# def config():
#     return jsonify(
#         TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID'],
#         TWILIO_NOTIFICATION_SERVICE_SID=os.environ.get('TWILIO_NOTIFICATION_SERVICE_SID', None),
#         TWILIO_API_KEY=os.environ['TWILIO_API_KEY'],
#         TWILIO_API_SECRET=bool(os.environ['TWILIO_API_SECRET']),
#         TWILIO_CHAT_SERVICE_SID=os.environ.get('TWILIO_CHAT_SERVICE_SID', None),
#         TWILIO_SYNC_SERVICE_SID=os.environ.get('TWILIO_SYNC_SERVICE_SID', 'default'),
#     )

# @app.route('/token', methods=['GET'])
# def randomToken():
#     return generateToken(fake.user_name())


# @app.route('/token', methods=['POST'])
# def createToken():
#     # Get the request json or form data
#     content = request.get_json() or request.form
#     # get the identity from the request, or make one up
#     identity = content.get('identity', fake.user_name())
#     return generateToken(identity)

# @app.route('/token/<identity>', methods=['POST', 'GET'])
# def token(identity):
#     return generateToken(identity)

# def generateToken(identity):
#     # get credentials for environment variables
#     account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     api_key = os.environ['TWILIO_API_KEY']
#     api_secret = os.environ['TWILIO_API_SECRET']
#     sync_service_sid = os.environ.get('TWILIO_SYNC_SERVICE_SID', 'default')
#     chat_service_sid = os.environ.get('TWILIO_CHAT_SERVICE_SID', None)

#     # Create access token with credentials
#     token = AccessToken(account_sid, api_key, api_secret, identity=identity)

#     # Create a Sync grant and add to token
#     if sync_service_sid:
#         sync_grant = SyncGrant(service_sid=sync_service_sid)
#         token.add_grant(sync_grant)

#     # Create a Video grant and add to token
#     video_grant = VideoGrant()
#     token.add_grant(video_grant)

#     # Create an Chat grant and add to token
#     if chat_service_sid:
#         chat_grant = ChatGrant(service_sid=chat_service_sid)
#         token.add_grant(chat_grant)

#     # Return token info as JSON
#     return jsonify(identity=identity, token=token.to_jwt().decode('utf-8'))




# # Notify - create a device binding from a POST HTTP request
# @app.route('/register', methods=['POST'])
# def register():
#     # get credentials for environment variables
#     account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     api_key = os.environ['TWILIO_API_KEY']
#     api_secret = os.environ['TWILIO_API_SECRET']
#     service_sid = os.environ['TWILIO_NOTIFICATION_SERVICE_SID']

#     # Initialize the Twilio client
#     client = Client(api_key, api_secret, account_sid)

#     # Body content
#     content = request.get_json()

#     content = snake_case_keys(content)

#     # Get a reference to the notification service
#     service = client.notify.services(service_sid)

#     # Create the binding
#     binding = service.bindings.create(**content)

#     print(binding)

#     # Return success message
#     return jsonify(message="Binding created!")

# # Notify - send a notification from a POST HTTP request
# @app.route('/send-notification', methods=['POST'])
# def send_notification():
#     # get credentials for environment variables
#     account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     api_key = os.environ['TWILIO_API_KEY']
#     api_secret = os.environ['TWILIO_API_SECRET']
#     service_sid = os.environ['TWILIO_NOTIFICATION_SERVICE_SID']

#     # Initialize the Twilio client
#     client = Client(api_key, api_secret, account_sid)

#     service = client.notify.services(service_sid)

#     # Get the request json or form data
#     content = request.get_json() if request.get_json() else request.form

#     content = snake_case_keys(content)

#     # Create a notification with the given form data
#     notification = service.notifications.create(**content)

#     return jsonify(message="Notification created!")

# @app.route('/<path:path>')
# def static_file(path):
#     return app.send_static_file(path)