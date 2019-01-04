#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from abc import ABCMeta, abstractmethod
from json import JSONDecodeError
from logging import getLogger

import inject as inject

from switchbot_hub.client.abstract_mqtt_client import AbstractMqttClient
from switchbot_hub.switchbot.abstract_bot_controller import AbstractBotController


class AbstractHubController(metaclass=ABCMeta):

    @abstractmethod
    def notify(self, event):
        pass


class HubController(AbstractHubController):
    logger = getLogger(__name__)

    @inject.autoparams()
    def __init__(self, mqttClient: AbstractMqttClient, switchBot: AbstractBotController):
        self.event = None

        if not isinstance(mqttClient, AbstractMqttClient):
            self.logger.error("mqtt client is not AbstractMqttClient. failed initialize HubController.")
            raise Exception("mqttClient is not AbstractMqttClient.")

        if not isinstance(switchBot, AbstractBotController):
            self.logger.error("switchBot is not AbstractBotController. failed initialize HubController.")
            raise Exception("switchBot is not AbstractBotController.")

        self.mqttClient = mqttClient
        self.mqttClient.setObserver(self)
        self.switchBot = switchBot

    def start(self):
        self.mqttClient.connect()

    def notify(self, event):
        self.logger.debug("Get event from IoT Core: {}".format(event))
        event_map = json.loads(event)
        self._event_router(event_map)

    def _event_router(self, event):

        if event['event'] == 'press':
            self.logger.info("process press event.")
            self._press_switch()
        elif event['event'] == 'turn_on':
            self.logger.info("process turn_on event.")
            self._turn_on()
        elif event['event'] == 'turn_off':
            self.logger.info("process turn_off event.")
            self._turn_off()
        elif event['event'] == 'status':
            self.logger.info("process status event")
            self._status()
        else:
            self.logger.info("Failed routing event process. :{}".format(event))

    def _press_switch(self):
        self.switchBot.press_switch()
        self.mqttClient.publish_telemetry('event success.', 'ackevent')

    def _turn_on(self):
        self.switchBot.turn_on_switch()

    def _turn_off(self):
        self.switchBot.turn_off_switch()

    def _status(self):
        result = self.switchBot.get_device_info()
        try:
            self.logger.info("get switchbot status {},{}".format(result["firmware"], result["battery"]))
            payload = json.dumps(result)
            self.mqttClient.publish_status(payload)
        except KeyError or TypeError:
            self.logger.warning("Failed get device info {}".format(result))
        except TypeError:
            self.logger.warning("Device info is type error. must be dict {}".format(result))
        except JSONDecodeError as e:
            self.logger.warning("Failed device info serialized to string by json.dumps ")
        # TODO NetWorkErrorHandling
