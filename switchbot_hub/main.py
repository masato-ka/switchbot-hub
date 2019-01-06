#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

import inject

from switchbot_hub.client.abstract_mqtt_client import AbstractMqttClient
from switchbot_hub.client.cloud_iot_core import CloudIoTCoreClient
from switchbot_hub.config import AbstractConfigurationManager
from switchbot_hub.config.SwitchBotHubConfigManager import SwitchBotHubConfigManager
from switchbot_hub.hub_controller import HubController
from switchbot_hub.switchbot.SwitchBotClient import SwitchBotClient
from switchbot_hub.switchbot.abstract_bot_controller import AbstractBotController

logger = logging.getLogger(__name__)


def setting_logger():
    fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)


def inject_config(binder):
    config_manager = SwitchBotHubConfigManager(os.path.dirname(os.path.abspath(__file__)))
    binder.bind(AbstractConfigurationManager, config_manager)
    binder.bind(AbstractMqttClient, CloudIoTCoreClient(config_manager))
    binder.bind(AbstractBotController, SwitchBotClient(config_manager))


def main():
    setting_logger()
    inject.configure(inject_config)
    hub_controller = HubController()
    logger.info("start up switchbot hub")
    hub_controller.start()


if __name__ == '__main__':
    main()
