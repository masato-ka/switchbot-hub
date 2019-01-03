#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractMqttClient(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        """When run connect method, Client connect to MQTT broker,
            and in state forever loop."""
        pass

    @abstractmethod
    def publish_telemetry(self, message):
        pass

    @abstractmethod
    def publish_status(self, message):
        pass
