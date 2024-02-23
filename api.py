from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import controller as controller

app = Flask(__name__)
MQTT_SERVER = "192.168.1.25"
MQTT_PATH = "device/control"
MQTT_USERNAME = 'matei'
MQTT_PASSWORD = '123456'

@app.route('/control_ac', methods=['POST'])
def control_ac():
    content = request.json
    # command = content['command']
    controller.encode_ac()  
    print(content)
    auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
    publish.single(MQTT_PATH, content, hostname=MQTT_SERVER, auth=auth)
    return jsonify({"status": "Command sent"}), 200

@app.route('/garage', methods=['POST'])
def control_garage():
    content = request.json
    command = content['command']
    controller.encode_ac()  
    print('garage')
    print(content)
    auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
    publish.single(MQTT_PATH, command, hostname=MQTT_SERVER, auth=auth)
    return jsonify({"status": "Command sent"}), 200


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)