#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import ssl
import time
from logging import getLogger

import inject
import jwt
import paho.mqtt.client as mqtt

from switchbot_hub.client.abstract_mqtt_client import AbstractMqttClient
from switchbot_hub.config import AbstractConfigurationManager

_minimum_backoff_time = 1
_MAXIMUM_BACKOFF_TIME = 32

logger = getLogger(__name__)


class CloudIoTCoreClient(AbstractMqttClient):
    _should_backoff = True

    _minimum_backoff_time = 1
    _MAXIMUM_BACKOFF_TIME = 32

    _observer = None
    _client = None

    @inject.autoparams()
    def __init__(self, config_manager: AbstractConfigurationManager):
        self.config_manager = config_manager
        self._project_id = self.config_manager.options.project_id
        self._cloud_region = self.config_manager.options.cloud_region
        self._registry_id = self.config_manager.options.registry_id
        self._device_id = self.config_manager.options.device_id

        self._private_key_file = self.config_manager.options.private_key_file
        self._algorithm = self.config_manager.options.algorithm
        self._ca_certs = self.config_manager.options.ca_certs_file

        self._mqtt_bridge_hostname = self.config_manager.options.mqtt_bridge_hostname
        self._mqtt_bridge_port = self.config_manager.options.mqtt_bridge_port

    def connect(self):
        """When run connect method, Client connect to MQTT broker,
            and in state forever loop."""

        jwt_iat = datetime.datetime.utcnow()
        jwt_exp_mins = 20
        self._client = self._get_client()
        while True:
            time.sleep(0.8)  # The magic number
            self._client.loop()
            if self.should_backoff:
                if self.minimum_backoff_time > self.MAXIMUM_BACKOFF_TIME:
                    logger.warn('Exceeded maximum backoff time. Giving up.')
                    break
                delay = self.minimum_backoff_time + random.randint(0, 1000) / 1000.0
                logger.info('Waiting for {} before reconnecting.'.format(delay))
                time.sleep(delay)
                self.minimum_backoff_time *= 2
                self._client.connect(self._mqtt_bridge_hostname, self._mqtt_bridge_port)
            seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
            if seconds_since_issue > 60 * jwt_exp_mins:
                logger.info('Refreshing token after {}s').format(seconds_since_issue)
                jwt_iat = datetime.datetime.utcnow()
                self._client = self._get_client()

    def setObserver(self, observer):
        self._observer = observer

    def publish_telemetry(self, message, subfolder=''):
        telemetry_topic = ('/devices/{}/events/{}').format(self._device_id, subfolder)
        self._client.publish(telemetry_topic, message, qos=1)
        logger.info('publish telemetry message subfolder:{}, message:{}'.format(subfolder, message))

    def publish_status(self, message):
        status_topic = ('/devices/{}/state').format(self._device_id)
        self._client.publish(status_topic, message, qos=1)
        logger.info('publish status message:{}'.format(message))

    def _error_str(self, rc):
        return '{}: {}'.format(rc, mqtt.error_string(rc))

    def _on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        logger.info('on_connect ' + mqtt.connack_string(rc))
        self.should_backoff = False
        self.minimum_backoff_time = 1

    def _on_disconnect(self, unused_client, unused_userdata, rc):
        logger.info('on_disconnect', self.error_str(rc))
        self.should_backoff = True

    def _on_publish(self, unused_client, unused_userdata, unused_mid):
        logger.info('on_publish')

    def _on_message(self, unused_client, unused_userdata, message):
        logger.info(message.payload.decode("utf-8"))
        self._observer.notify(message.payload)

    def _get_client(self):
        client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                .format(
                self._project_id,
                self._cloud_region,
                self._registry_id,
                self._device_id)))
        client.username_pw_set(
            username='unused',
            password=self._create_jwt(
                self._project_id, self._private_key_file, self._algorithm))

        # TODO Enable SSL/TLS support.
        client.tls_set(ca_certs=self._ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

        client.on_connect = self._on_connect
        client.on_publish = self._on_publish
        client.on_disconnect = self._on_disconnect
        client.on_message = self._on_message
        client.connect(self._mqtt_bridge_hostname, self._mqtt_bridge_port)

        mqtt_config_topic = '/devices/{}/config'.format(self._device_id)
        client.subscribe(mqtt_config_topic, qos=1)

        mqtt_command_topic = '/devices/{}/commands/#'.format(self._device_id)
        client.subscribe(mqtt_command_topic, qos=0)

        return client

    def _create_jwt(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'aud': project_id
        }

        with open(private_key_file, 'r') as f:
            private_key = f.read()

        logger.debug('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

        return jwt.encode(token, private_key, algorithm=algorithm)
