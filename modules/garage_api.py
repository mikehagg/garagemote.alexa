# ********************************************************************************************
# Copyright Mike Haggerty (2019)
# Feel free to shameless steal, but please apply credit where credit is due!
# ********************************************************************************************

import boto3
import json
import time
import os

# GarageDoor Specific Information
host = os.environ["IOT_ENDPOINT"]
clientId = "AlexaLambda"
thingName = os.environ["THING_NAME"]
topic = os.environ["THING_TOPIC"]


def get_shadow():
    client = boto3.client('iot-data', region_name='us-east-1')
    response = client.get_thing_shadow(thingName='GarageDoor')
    streaming_body = response["payload"]
    raw_data_bytes = streaming_body.read()  # rawDataBytes is of type 'bytes' in, Python 3.x specific
    raw_data_string = raw_data_bytes.decode('utf-8')  # Python 3.x specific
    data = json.loads(raw_data_string)
    return data


def set_garage_desired_state(door, new_state):
    data = get_shadow()
    for item in data['state']['reported']:
        if 'name' not in data['state']['reported'][item]:
            continue
        if data['state']['reported'][item]['name'] == door:
            desired_json = {"state": {"desired": {item: {"status": new_state}}}}
            # print("Sending desired state to garage..." + json.dumps(desired_json))
            send_message_to_garage_shadow(json.dumps(desired_json))
            # Sleeping to allow time for shadow to update.  Otherwise you may get a report of an incorrect state.
            time.sleep(0.33)


def get_garage_door_status(which_door):
    json_state = get_shadow()
    # print("Shadow JSON: " + json.dumps(json_state))
    for item in json_state['state']['reported']:
        if 'name' not in json_state['state']['reported'][item]:
            continue
        if json_state['state']['reported'][item]['name'] == which_door:
            door_status = json_state['state']['reported'][item]['status']
            return door_status


def get_garage_temp():
    client = boto3.client('iot-data', region_name='us-east-1')
    response = client.get_thing_shadow(thingName='GarageDoor')
    streaming_body = response["payload"]
    raw_data_bytes = streaming_body.read()  # rawDataBytes is of type 'bytes' in, Python 3.x specific
    raw_data_string = raw_data_bytes.decode('utf-8')  # Python 3.x specific
    json_state = json.loads(raw_data_string)
    temp = json_state['state']['reported']['garage_temp']  # Python 3.x specific
    return temp


def get_garage_humidity():
    client = boto3.client('iot-data', region_name='us-east-1')
    response = client.get_thing_shadow(thingName='GarageDoor')
    streaming_body = response["payload"]
    raw_data_bytes = streaming_body.read()  # rawDataBytes is of type 'bytes' in, Python 3.x specific
    raw_data_string = raw_data_bytes.decode('utf-8')  # Python 3.x specific
    json_state = json.loads(raw_data_string)
    humidity = json_state['state']['reported']['garage_humidity']  # Python 3.x specific
    return humidity


def get_garage_heat_index():
    client = boto3.client('iot-data', region_name='us-east-1')
    response = client.get_thing_shadow(thingName='GarageDoor')
    streaming_body = response["payload"]
    raw_data_bytes = streaming_body.read()  # rawDataBytes is of type 'bytes' in, Python 3.x specific
    raw_data_string = raw_data_bytes.decode('utf-8')  # Python 3.x specific
    json_state = json.loads(raw_data_string)
    heat_index = json_state['state']['reported']['garage_heat_index']  # Python 3.x specific
    return heat_index


def send_message_to_garage_shadow(message):
    shadow_client = boto3.client('iot-data', 'us-east-1')
    print("Executing update to shadow...")
    response = shadow_client.update_thing_shadow(thingName=thingName, payload=message)
    print('Published topic %s: %s\n' % (thingName, message))
    print("Response from client : " + json.dumps(response['payload'].read().decode('utf-8')))
