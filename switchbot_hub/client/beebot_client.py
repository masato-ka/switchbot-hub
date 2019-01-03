#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from paho.mqtt import client

from switchbot_hub.client.abstract_mqtt_client import AbstractMqttClient

HOST = 'mqtt.beebotte.com'
PORT = 8883
CA_CERTS_FILE_NAME = 'mqtt.beebotte.com.pem'
BEEBOT_TOKEN = 'token_PwpGQqH8XSTeNVPy'
TOPIC = 'switch/switch'


class BeebotClient(AbstractMqttClient):

    def __init__(self):
        self.observer = None
        self.client = client.Client(protocol=client.MQTTv311)

    def on_connect(self, client, userdata, flags, respons_code):
        print('status {0}'.format(respons_code))

    def on_message(self, client, userdata, msg):
        self.observer.notify(msg.payload)

        print(msg.topic + ' ' + str(msg.payload))
        print(msg.payload.decode("utf-8"))

    def on_disconnect(self, client, userdata, rc):
        print("disconnected with rtn code [%d]" % (rc))

    def setObserver(self, observer):
        self.observer = observer

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set('token:%s' % BEEBOT_TOKEN)
        self.client.tls_set(CA_CERTS_FILE_NAME)
        self.client.connect(HOST, PORT, 360)
        self.client.subscribe(TOPIC)
        self.client.loop_forever()

    def publish_telemetry(self, message):
        pass

    def publish_status(self, message):
        pass
