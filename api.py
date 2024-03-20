from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import controller as controller
import json
import socketio
import logging
import hashlib

app = Flask(__name__)
MQTT_SERVER = "192.168.1.25"
MQTT_PATH = "device/control"
MQTT_USERNAME = 'matei'
MQTT_PASSWORD = '123456'
pi_serial_number = '10000000f3ec5d31'

sio = socketio.Client(logger=True, engineio_logger=True)

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
