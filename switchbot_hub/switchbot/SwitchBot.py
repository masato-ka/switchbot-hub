#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import struct
import threading

from bluepy.btle import Peripheral, DefaultDelegate
from switchbot.abstract_bot_controller import AbstractBotController

NOTIFY_CONTROLL_HANDLER = 0x0014

SWITCH_CONTROLL_HANDLER = 0x0016

PRESS_EVENT = "570100"
TURN_ON_EVENT = "570101"
TURN_OFF_EVENT = "570102"
GET_INFO_EVENT = "570105"

START_NOTIFY_EVENT = "0100"
STOP_NOTIFY_EVENT = "0000"

SWITCH_CONTROLL_CHARACTERISTIC = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
SWITCH_NOTIFY_CHARACTERISTIC = "cba20003-224d-11e6-9fb8-0002a5d5c51b"

SWITCH_CONTROLL_SERVICE = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"


class InformationDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)
        self.observer = None

    def setObserver(self, observer):
        self.observer = observer

    def handleNotification(self, cHandle, data):
        if cHandle == 0x13:
            self.observer._notify(data)
        else:
            print(" Other notification")


class SwitchBot(AbstractBotController):

    def __init__(self, config):
        self.device_id = config.switchbot_id
        self.version = None
        self.battery = None

    def press_switch(self):
        self._move_switch(PRESS_EVENT)

    def turn_on_switch(self):
        self._move_switch(TURN_ON_EVENT)

    def turn_off_switch(self):
        self._move_switch(TURN_OFF_EVENT)

    def get_device_info(self):
        p = Peripheral(self.device_id, "random")
        self.version = None
        self.battery = None
        self._start_notification(p)
        recv_thread = self.__spawn_recv_thread(p)
        p.writeCharacteristic(SWITCH_CONTROLL_HANDLER, binascii.a2b_hex(GET_INFO_EVENT), False)
        recv_thread.join()
        self._stop_notification(p)
        p.disconnect()
        return (self.version, self.battery)

    def _notify(self, payload):
        self.version = "".join([x + "." for x in str(struct.unpack('B', payload[2])[0])])[:-1]
        btr = struct.unpack('B', payload[1])
        self.battery = btr[0] / 255.0 if btr[0] is not 0 else 0

    def _start_notification(self, p):
        information_delegate = InformationDelegate()
        information_delegate.setObserver(self)
        p.setDelegate(information_delegate)
        p.writeCharacteristic(NOTIFY_CONTROLL_HANDLER, binascii.a2b_hex(START_NOTIFY_EVENT), True)

    def _stop_notification(self, p):
        p.writeCharacteristic(0x0014, binascii.a2b_hex(STOP_NOTIFY_EVENT), True)

    def __spawn_recv_thread(self, p):
        def recv_thread():
            p.waitForNotifications(1.0)

        thread = threading.Thread(target=recv_thread, name="rect_thread")
        thread.start()
        return thread

    def _move_switch(self, event):
        p = Peripheral(self.device_id, "random")
        self._send_event(p, SWITCH_CONTROLL_SERVICE, SWITCH_CONTROLL_CHARACTERISTIC, event)
        p.disconnect()

    def _send_event(self, p, service, characteristic, event):
        hand_service = p.getServiceByUUID(service)
        hand = hand_service.getCharacteristics(characteristic)[0]
        hand.write(binascii.a2b_hex(event))
