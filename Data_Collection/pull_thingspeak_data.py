import requests
import json

Previous_Session = 'https://api.thingspeak.com/channels/1277562/fields/1/last.json'
request = requests.get(Previous_Session).json()
float_response = float(request['field1'])

print(float_response)
