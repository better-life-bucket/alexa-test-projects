from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.utils.request_util import get_slot
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import boto3

sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Bem vindo ao Skill Localizador de Objetos da Better Life."

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better-Life", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
def hello_world_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Olá!"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better-Life", speech_text)).set_should_end_session(
        True)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("GetObjectLocation"))
def get_object_intent_handler(handler_input):
    # type: (HandlerInput) -> Response1
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('localizador-objetos-table')
    user_id = handler_input.request_envelope.session.user.user_id
    
    ### Remove Later - For testing purposes ###
    user_id = "0"

    response = table.get_item(Key={"user-id":user_id})

    if 'Item' not in response.keys():
        speech_text = "Você ainda não cadastrou nenhum objeto. Para começar a armazenar a localização de seus objetos, por exemplo, depois de abrir a skill, pode dizer, meu celular está no armário."
        handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better-Life", speech_text)).set_should_end_session(
        True)
        return handler_input.response_builder.response


    object_locations = response['Item']['objlocation']

    slots = handler_input.request_envelope.request.intent.slots
    #object_locations = {"celular": f"Em cima do criado mudo.", "carteira": f"Dentro do armário da sala."}

    slot_obj = get_slot(handler_input, "objeto")
    object_name = slot_obj.value
    if object_name is None:
        speech_text = "Eu não consegui identificar o objeto que você está buscando."
    else:
        if object_name in object_locations.keys():
            speech_text = f"Eu localizei {object_name}! Está {object_locations[object_name]}."
        else:
            speech_text = f"Desculpe, eu não sei onde está {object_name}. Caso você encontre, pode me avisar falando, Alexa, cadastrar {object_name} está em determinado lugar no localizador de objetos, e da próxima vez, eu lembrarei."

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better-Life", speech_text)).set_should_end_session(
        True)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("InsertObjectLocation"))
def insert_object_intent_handler(handler_input):
    # type: (HandlerInput) -> Response1
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('localizador-objetos-table')
    user_id = handler_input.request_envelope.session.user.user_id
    
    ### Remove Later - For testing purposes ###
    user_id = "0"

    response = table.get_item(Key={"user-id":user_id})

    slots = handler_input.request_envelope.request.intent.slots
    # object_locations = {"celular": f"Em cima do criado mudo.", "carteira": f"Dentro do armário da sala."}

    slot_obj = get_slot(handler_input, "objeto")
    slot_loc = get_slot(handler_input, "location")

    object_name = slot_obj.value
    object_location = slot_loc.value

    if object_name is None: #Não identificou objeto
        speech_text = "Eu não consegui identificar o objeto que você está inserindo."
    else:   #Identificou objeto
        if object_location is None: #não identificou localização
            speech_text = f"Eu não consegui identificar a localização de {object_name}. Por favor, tente novamente."
        else: #identificou localização
            if 'Item' not in response.keys(): #usuário não existente no BD
                #Creating new item in Dynamo
                object_locations = {object_name: object_location}

                response = table.put_item(
                    Item={
                            'user-id': user_id,
                            'objlocation': object_locations
                        }
                    )
            else: #Usuário já existente no BD
                #Updating an item in Dynamo
                object_locations = response['Item']['objlocation']
                if object_name in object_locations.keys(): #Objeto ja cadastrado no BD
                    old_object_location = object_locations[object_name]
                    object_locations[object_name] = object_location
                    speech_text = f"{object_name} está agora {object_location}. Antes, {object_name} estava {old_object_location}."
                else: #Um novo objeto registrado para o usuario
                    object_locations[object_name] = object_location
                    speech_text = f"{object_name} está agora {object_location}."

                response = table.update_item(
                    Key={
                        'user-id': user_id
                    },
                    UpdateExpression="set objlocation=:o",
                    ExpressionAttributeValues={
                        ':o': object_locations
                    },
                    ReturnValues="UPDATED_NEW"
                )
                

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better-Life", speech_text)).set_should_end_session(
        True)
    return handler_input.response_builder.response



'''
Built-in intents
'''
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Você pode dizer Olá!"

    handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
        SimpleCard("Better-Life", speech_text))
    return handler_input.response_builder.response

@sb.request_handler(
    can_handle_func=lambda handler_input :
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Até logo!"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Better Life", speech_text)).set_should_end_session(
            True)
    return handler_input.response_builder.response

'''
Although you cannot return a response with any speech, card or directives after receiving a SessionEndedRequest, 
the SessionEndedRequestHandler is a good place to put your cleanup logic. 
Type or paste the following code into your hello_world.py file, after the previous handler.
'''
@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    # any cleanup logic goes here

    return handler_input.response_builder.response

'''
The following sample adds a catch all exception handler to your skill, 
to ensure the skill returns a meaningful message in case of all exceptions. 
Type or paste the following code into your hello_world.py file, after the previous handler.
'''
@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    # Log the exception in CloudWatch Logs
    print(exception)

    speech = "Sorry, I didn't get it. Can you please say it again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


'''
The Lambda handler is the entry point for your AWS Lambda function. 
The following code example creates a Lambda handler function to route 
all inbound requests to your skill. The Lambda Handler function creates 
an SDK skill instance configured with the request handlers that you just created.
'''

handler = sb.lambda_handler()
