#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import configargparse

from switchbot_hub.config.AbstractConfigurationManager import AbstractConfigrationManager


class SwitchBotHubConfigManager(AbstractConfigrationManager):

    def __init__(self, current_path):
        self.default_config_path = os.path.join(current_path, '..', 'switchbot-hub.conf')
        self.default_private_key_path = os.path.join(current_path, '..', 'resources', 'rsa_private.pem')
        self.default_ca_certs_path = os.path.join(current_path, '..', 'resources', 'roots.pem')
        self.parser = configargparse.ArgParser(default_config_files=[self.default_config_path])

        self.parser.add('-c', '--my-config',
                        is_config_file=True,
                        default=self.default_config_path,
                        help='config file path')
        self.parser.add('-v', help='verbose', action='store_true')
        # SwitchBot setting.
        self.parser.add('--switchbot_id', help='switchbot MAC ID.')

        # GCP CloudIoTCore setting
        self.parser.add('--project_id',
                        required=True,
                        help='GCP Cloud project name',
                        env_var='GOOGLE_CLOUD_PROJECT')
        self.parser.add('--cloud_region',
                        required=True,
                        help='GCP Cloud region',
                        env_var='GOOGLE_CLOUD_REGION')
        self.parser.add('--registry_id',
                        required=True,
                        help='Cloud IoT Core registry id',
                        env_var='GOOGLE_IOT_CORE_REGISTRY')
        self.parser.add('--device_id',
                        required=True,
                        help='Cloud IoT Core registry id',
                        env_var='GOOGLE_IOT_CORE_DEVICE_ID')
        self.parser.add('--private_key_file',
                        default=self.default_private_key_path,
                        help='Path to private key file.',
                        env_var='PRIVATE_KEY_FILE')
        self.parser.add('--ca_certs_file',
                        default=self.default_ca_certs_path,
                        help='Path to private key file.',
                        env_var='CA_CERTS_FILE')
        self.parser.add('--algorithm',
                        default='RS256',
                        help='Which encryption algorithm to use to generate the JWT.',
                        choices=('RS256', 'ES256'))
        self.parser.add('--mqtt_bridge_hostname',
                        default='mqtt.googleapis.com',
                        help='MQTT bridge hostname.',
                        env_var='GOOGLE_IOT_CORE_HOSTNAME')
        self.parser.add('--mqtt_bridge_port',
                        default=8883,
                        type=int,
                        help='MQTT bridge port.',
                        env_var='GOOGLE_IOT_CORE_PORT',
                        choices=(8883, 443))
        self.parser.add('--jwt_expires_minutes',
                        default=20,
                        type=int,
                        help=('Expiration time, in minutes, for JWT tokens.'))

        self.options = self.parser.parse_args()

    def load_configration(self):
        pass
