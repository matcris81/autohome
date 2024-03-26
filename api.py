#!/home/matcris81/webserver/venv/bin/python

from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import controller as controller
import json
import socketio
import logging
import hashlib
import time

app = Flask(__name__)
MQTT_SERVER = "192.168.1.25"
MQTT_PATH = "device/control"
MQTT_USERNAME = 'matei'
MQTT_PASSWORD = '123456'
pi_serial_number = '10000000f3ec5d31'

sio = socketio.Client(logger=True, engineio_logger=True)

def is_network_available(host="192.168.1.3", port=3000, timeout=10):
    """Check if the network is available by attempting to connect to a specified host/port."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"Network not available yet: {ex}")
        return False

def wait_for_network_and_connect_to_nestjs(attempts=5, delay=10):
    """Wait for the network to be available by checking connectivity to the NestJS server."""
    for attempt in range(attempts):
        if is_network_available():
            print("Network is available. Attempting to connect to NestJS server.")
            connect_to_nestjs()
            break
        else:
            print(f"Network not available. Waiting for {delay} seconds before retrying...")
            time.sleep(delay)
    else:
        print("Failed to connect to the NestJS server after several attempts.")

def connect_to_nestjs():
    connection_url = f'http://192.168.1.3:3000?deviceId={pi_serial_number}'
    sio.connect(connection_url)
    print('Connected to NestJS server with deviceId and accessToken.')

@sio.event
def connect():
    token = controller.generate_token(pi_serial_number)
    print('Connection established')
    print(pi_serial_number)
    print(token) 
    sio.emit('message', 'Pi is online')
    sio.emit('register', {'deviceId': pi_serial_number, 'accessToken': token})


@sio.event
def disconnect():
    print('Disconnected from server')

# sio.connect('https://your-nestjs-domain.com')
# sio.connect('http://192.168.3.33:3000')

# @app.route('/control_ac', methods=['POST'])
@sio.on('control_ac')
def control_ac(data):
    # content = request.json
    # json_string = json.dumps(content)
    print(data)
#    command = data['command']
#    print(command)
    auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
    publish.single(MQTT_PATH, data, hostname=MQTT_SERVER, auth=auth)
    return jsonify({"status": "Command sent"}), 200

# @app.route('/garage', methods=['POST'])
@sio.on('control_garage')
def control_garage(data):
    # content = request.json
    # command = content['command']
    print(data)
#    command = data['command']
#    print(command)
    auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
    publish.single(MQTT_PATH, data, hostname=MQTT_SERVER, auth=auth)
    return jsonify({"status": "Command sent"}), 200



if __name__ == '__main__':
   connect_to_nestjs()
   app.run(host='0.0.0.0', port=6000)
