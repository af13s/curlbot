import dialogflow_v2

LANGUAGE_CODE = 'en'
PROJECT_ID = AGENT_ID = "newagent-hrmeto"
AGENT_PATH = "projects/newagent-hrmeto/agent"
DEFAULT_KIND="KIND_MAP"
DEFAULT_NAME_APPENDAGE = "product"
LOOKUP_INTENT_ID = "4091c1b0-d2d2-406a-a2bc-ed9253b110f6"


DEFAULT_CREDENTIALS = None

COMPANY_ENTITY_NAME = "HairCompany"

PRODUCT_LOOKUP_DISPLAY_NAME = "Product Lookup"

class DialogFlowClient:

    entity_type_list = None
    phone_number = None

    def __init__(self, phone_number):
        DialogFlowClient.phone_number = phone_number

    def get_session(self,phone_number):
        session_client = dialogflow_v2.SessionsClient(credentials=DEFAULT_CREDENTIALS)
        session = session_client.session_path( AGENT_ID, DialogFlowClient.phone_number)

        return {
            "client" : session_client,
            "session" : session
        }


    def analyze_msg(self, message):

        session_client = self.get_session()["client"]
        session = self.get_session()["session"]

        text_message = dialogflow_v2.types.TextInput(
            text=message,
            language_code=LANGUAGE_CODE
        )

        query_input = dialogflow_v2.types.QueryInput(text=text_message)
        response = session_client.detect_intent(query_input=query_input,session=session)
        print(response)

        return self.get_intent(response), self.get_params(response)
    
    def extract_intent(self, response):
        return response.query_result.intent.display_name

    def extract_params(self, response):
        params = {}
        for param in response.query_result.parameters:
            params[param] = response.query_result.parameters[param]
        return params
    
    def get_entity_client(self):
        client = dialogflow_v2.EntityTypesClient(credentials=DEFAULT_CREDENTIALS)
        return client

    def create_entity(self, brand_name, entities, agent=AGENT_PATH, language=LANGUAGE_CODE, kind=DEFAULT_KIND):
        client = self.get_entity_client()
        entity_type = {
            "name" : "",
            "display_name": brand_name.replace(" ", "").lower()+DEFAULT_NAME_APPENDAGE,
            "entities" : entities,
            'kind': kind,
        }
        response = client.create_entity_type(parent=agent, entity_type=entity_type)
        print(response)
    
    def update_entity(self, entity_path, entity_name, entities, kind=DEFAULT_KIND):
        client = self.get_entity_client()
        entity_type = {
            'name': entity_path,
            'display_name': entity_name,
            'kind': kind,
            'entities': entities,
        }
        response = client.update_entity_type(entity_type)
        print(response)

    ## not ready yet, how to interate and get id's
    # def get_entity_list(self, agent=AGENT_PATH):

    #     if entity_type_list:
    #         pass
    #     else:
    #         client = get_entity_client()
    #         entity_type_list = client.list_entity_types(parent=agent)

    def format_entity_type(self, brand_name):
        formatted_name = brand_name.replace(" ", "").lower()+DEFAULT_NAME_APPENDAGE
        return formatted_name

    def get_intent_client(self):
        client = dialogflow_v2.IntentsClient(credentials=DEFAULT_CREDENTIALS)
        return client
    
    def create_product_lookup_intent(self, brand_name, product_name, extra_text=""):
        client = self.get_intent_client()

        parts = [

            dialogflow_v2.types.Intent.TrainingPhrase.Part(text=extra_text),

            dialogflow_v2.types.Intent.TrainingPhrase.Part(
                text=" ",
            ),

            dialogflow_v2.types.Intent.TrainingPhrase.Part(
                text=brand_name,
                entity_type='@{}'.format(COMPANY_ENTITY_NAME),
                alias=COMPANY_ENTITY_NAME
            ),

            dialogflow_v2.types.Intent.TrainingPhrase.Part(
                text=" ",
            ),
            
            dialogflow_v2.types.Intent.TrainingPhrase.Part(
                text=product_name,
                entity_type='@{}'.format(self.format_entity_type(brand_name)),
                alias=self.format_entity_type(brand_name)
            )
        ]

        training_phrase = dialogflow_v2.types.Intent.TrainingPhrase(parts=parts)

        intent = {
            "name" : "projects/{}/agent/intents/{}".format(PROJECT_ID, LOOKUP_INTENT_ID),
            "display_name": PRODUCT_LOOKUP_DISPLAY_NAME,
            "training_phrases": [training_phrase]
        }
        
        response = client.update_intent(intent=intent, language_code=LANGUAGE_CODE)

        print(response)






        

