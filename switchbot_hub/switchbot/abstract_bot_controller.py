#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractBotController(metaclass=ABCMeta):

    @abstractmethod
    def press_switch(self):
        pass

    @abstractmethod
    def turn_on_switch(self):
        pass

    @abstractmethod
    def turn_off_switch(self):
        pass

    @abstractmethod
    def get_device_info(self):
        return (None, None)
