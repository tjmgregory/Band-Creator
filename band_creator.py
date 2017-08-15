import json
from random import randint

import requests


def handler(event, context):
    request = event['request']

    if request['type'] == "LaunchRequest":
        return handle_launch()
    elif request['type'] == "IntentRequest":
        if request['intent']['name'] == "BandName":
            return handle_intent()
        elif request['intent']['name'] == "AMAZON.HelpIntent":
            return handle_help()
        elif request['intent']['name'] == "AMAZON.StopIntent":
            return handle_stop()
    elif request['type'] == "SessionEndedRequest":
        return handle_session_ended()


def handle_launch():
    return respond("Hey there, ask me to create a band name.", False)


def handle_intent():
    response = requests.get("http://bandname.filiplundby.dk/api/v1/sentence")
    name = json.loads(response.text)[0]

    if len(name) == 0:
        return respond("I failed to be creative, I'm sorry.", True)

    return respond("A good name is: " + name, True)


def handle_help():
    return respond("I'm not the smartest bot, but try asking me to create you a band name.", False)


def handle_stop():
    goodbyes = [
        "See ya.",
        "Ciao.",
        "Goodbye",
        "Bye."
    ]
    return respond(goodbyes[randint(0, 3)], True)


def handle_session_ended():
    pass


def respond(response, end):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': response
            },
            'shouldEndSession': end
        }
    }
