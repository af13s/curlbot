def record_message(message, phone_number, tablename="messages"):
   item = {
      "user_phone": phone_number,
      "message": message,
   }

  database.add_table_entry(tablename, item)

def record_product_search(phone_number, product_name, brand_name, tablename="searches"):
   item = {
      "user_phone": phone_number,
      "product_name": product_name,
      "brand_name": brand_name,
   }

   database.add_table_entry(tablename, item)

def record_user_info(phone_number, curl_type, **kwargs):
   item = {
      "user_phone": phone_number,
      "curl_type": curl_type,
   }

   for key, value in kwargs.items():
      item[key] = value
   
   database.add_table_entry(tablename, item)


def ingredients_analyzer(ingredients_string):

   bad_ingredients = []
   ingredients_list = ingredients_string.split(",")

   for ingredient in ingredients_list:
      if ingredient_is_harmful(ingredient):
         bad_ingredients.append({
            ingredient: ingredients_info(ingredient)
         })
   
   report = report_format(bad_ingredients) 

   return report


def generate_response(phone, message):
   record_message(phone, message)

   intent, variables = dialogflow(message)
   reply = None

   # psuedo
   if intent == product_lookup:
      try:
         record_product_search(phone_number=phone, product_name=variable["product_name"], brand_name=variable["brand_name"])
      except Exception as e:
         print("Error occured trying to add new entry %s", s)

      ingredients = db_search(key=variable["product_name"], range=variable["brand_name"])["ingredients"]
      reply = ingredients_analyzer(ingredients)
      


   
   if intent == hair_recommendation:
      try: 
         record_user_info(phone_number, curl_type, ...)
      except Exception as e:
         print("Error occured trying to add new entry %s", s)

      recommendation = dataset_search(hair_type=variables["hair_type"])
      reply = recommendation


   
   string = "Hello from twilio\n "
   string += message

   return string




####

### TODO ### 

Store all user messages in the database and timestamp the messages

schema phone_number: string
       message: string
       datetime: string
       epoch_timestamp: number

train dialogflow to understand the messages - take the names in the database and create permutations for dialogflow to train on

take a message
extract the variables - use dialogflow to recognize the entities
discover the intent - sending the message to dialog flow
response based on intent - add fulfillment webhook to the product. get the intent and use that to form the logic




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