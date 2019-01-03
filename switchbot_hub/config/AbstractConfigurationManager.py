#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractConfigrationManager(metaclass=ABCMeta):

    @abstractmethod
    def load_configration(self):
        pass
