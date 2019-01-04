from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import MagicMock

import inject

from switchbot_hub.client.abstract_mqtt_client import AbstractMqttClient
from switchbot_hub.hub_controller import HubController
from switchbot_hub.switchbot.abstract_bot_controller import AbstractBotController

mqtt_client_mock = MagicMock(spec=AbstractMqttClient)
bot_controll = MagicMock(spec=AbstractBotController)


def inject_config(binder):
    # binder.bind(AbstractConfigurationManager, config_manager)
    binder.bind(AbstractMqttClient, mqtt_client_mock)
    binder.bind(AbstractBotController, bot_controll)


class TestHubController(TestCase):

    def setUp(self):
        inject.configure_once(inject_config)
        self.target = HubController()

    def test_start(self):
        self.target.start()
        mqtt_client_mock.connect.assert_called_with()

    def test_notify_normal01(self):
        mock = MagicMock()
        self.target._event_router = mock
        self.target.notify('{"event":"press"}')
        mock.assert_called_once_with({"event": "press"})

    def test_notify_abnormal01(self):
        try:
            self.target.notify('not json type string')
            self.faile()
        except JSONDecodeError as e:
            pass

    def test_notify_abnormal02(self):
        try:
            self.target.notify({"event": "press"})
            self.faile()
        except TypeError as e:
            pass

    def test_notify_abnormal03(self):
        try:
            self.target.notify('{"command":"press"}')
            self.faile()
        except KeyError as e:
            pass

    def test__event_router_normal01(self):
        mock = MagicMock()
        self.target._press_switch = mock
        test = {"event": "press"}
        self.target._event_router(test)
        mock.assert_called_with()

    def test__event_router_normal02(self):
        mock = MagicMock()
        self.target._turn_on = mock
        test = {"event": "turn_on"}
        self.target._event_router(test)
        mock.assert_called_with()

    def test__event_router_normal03(self):
        mock = MagicMock()
        self.target._turn_off = mock
        test = {"event": "turn_off"}
        self.target._event_router(test)
        mock.assert_called_with()

    def test__event_router_normal04(self):
        mock = MagicMock()
        self.target._status = mock
        test = {"event": "status"}
        self.target._event_router(test)
        mock.assert_called_with()

    def test__event_router_abnormal01(self):
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        test = {"event": "hoge"}
        self.target._event_router(test)
        mock_logger.info.assert_called_once_with("Failed routing event process. :{}".format(test))

    def test__event_router_abnormal02(self):
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        test = {"event": 123}
        self.target._event_router(test)
        mock_logger.info.assert_called_once_with("Failed routing event process. :{}".format(test))

    def test__event_router_abnormal03(self):
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        test = {"event": True}
        self.target._event_router(test)
        mock_logger.info.assert_called_once_with("Failed routing event process. :{}".format(test))

    def test__press_switch_normal01(self):
        self.target._press_switch()
        bot_controll.press_switch.assert_called_with()
        mqtt_client_mock.publish_telemetry.assert_called_once_with('event success.', 'ackevent')

    def test__turn_on_normal01(self):
        self.target._turn_on()
        bot_controll.turn_on_switch.assert_called_with()
        mqtt_client_mock.publish_telemetry.assert_called_once_with('event success.', 'ackevent')

    def test__turn_off_normal01(self):
        self.target._turn_off()
        bot_controll.turn_off_switch.assert_called_with()
        mqtt_client_mock.publish_telemetry.assert_called_once_with('event success.', 'ackevent')

    def test__status_normal01(self):
        test = {"battery": 1.0, "firmware": "4.4"}
        bot_controll.get_device_info.return_value = test
        self.target._status()
        bot_controll.get_device_info.assert_called_with()
        mqtt_client_mock.publish_status.assert_called_once_with('{"battery": 1.0, "firmware": "4.4"}')

    def test__status_abnormal01(self):
        test = {}
        bot_controll.get_device_info.return_value = test
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        self.target._status()
        self.target.logger.warning.assert_called_with("Failed get device info {}".format(test))

    def test__status_abnormal02(self):
        test = {"battery": 1.0}
        bot_controll.get_device_info.return_value = test
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        self.target._status()
        self.target.logger.warning.assert_called_with("Failed get device info {}".format(test))

    def test__status_abnormal03(self):
        test = {"firmware": "4.4"}
        bot_controll.get_device_info.return_value = test
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        self.target._status()
        self.target.logger.warning.assert_called_with("Failed get device info {}".format(test))

    def test__status_abnormal04(self):
        test = '"firmware":"4.4", "battery":1.0'
        bot_controll.get_device_info.return_value = test
        mock_logger = MagicMock()
        self.target.logger = mock_logger
        self.target._status()
        self.target.logger.warning.assert_called_with("Device info is type error. must be dict {}".format(test))
