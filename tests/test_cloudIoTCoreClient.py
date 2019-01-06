from unittest import TestCase
from unittest.mock import MagicMock

from switchbot_hub.client.cloud_iot_core import CloudIoTCoreClient
from switchbot_hub.config.SwitchBotHubConfigManager import SwitchBotHubConfigManager


class TestCloudIoTCoreClient(TestCase):

    def setUp(self):
        self.mock_configure = MagicMock(spec=SwitchBotHubConfigManager)
        self.target = CloudIoTCoreClient(self.mock_configure)

    def test_connect(self):
        pass

    def test_setObserver(self):
        pass

    def test_publish_telemetry(self):
        self.target._client = MagicMock()
        self.target._device_id = "mydevice"
        expect_subfolder = "subfolder"
        expect_topic = ('/devices/{}/events/{}').format(self.target._device_id, expect_subfolder)
        expect_payload = '{"ret":"hogehoge"}'
        self.target.publish_telemetry(expect_payload, expect_subfolder)
        self.target._client.publish.assert_called_once_with(expect_topic, expect_payload, pos=1)

    def test_publish_status(self):
        pass

    def test__error_str(self):
        pass

    def test__on_connect(self):
        pass

    def test__on_disconnect(self):
        pass

    def test__on_publish(self):
        pass

    def test__on_message(self):
        pass

    def test__get_client(self):
        pass

    def test__create_jwt(self):
        pass
