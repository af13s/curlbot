import dialogflow_v2

LANGUAGE_CODE = 'en-US'
AGENT_ID = "newagent-hrmeto"

class DiaglogFlowClient:

    

    def __init__(self, phone_number):
        self.session_client = dialogflow_v2.SessionsClient()
        self.session = self.session_client.session_path( AGENT_ID, phone_number)

    def analyze_msg(self, message):
        text_message = dialogflow.types.TextInput(
            text=message,
            language_code=LANGUAGE_CODE
        )

        query_input = dialogflow.types.QueryInput(text=text_message)

        response = session_client.detect_intent(query_input=query_input,session=self.session)
        print(response)

        return self.get_intent(response), self.get_params(response)
    
    def get_intent(response):
        return response.query_result.intent.display_name

    def get_params(response):
        params = {}
        for param in response.query_result.parameters:
            params[param] = response.query_result.parameters[param]
        return params




        
