#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from logging import getLogger

from switchbot_hub.switchbot.abstract_bot_controller import AbstractBotController

logger = getLogger(__name__)


class MockBotController(AbstractBotController):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def press_switch(self):
        logger.info('press switch!')

    def turn_on_switch(self):
        logger.info('turn on switch!')

    def turn_off_switch(self):
        logger.info('turn off switch!')

    def get_device_info(self):
        return ('4.4', 1.0)
