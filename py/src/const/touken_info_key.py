# coding: utf-8

__all__ = ['ToukenInfoKey']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from enum import Enum


class ToukenInfoKey(Enum):
    UID = 'uid'
    NAME_EN = 'name'
    NAME = 'display_name'
    FACTION = 'faction'
    KIND = 'kind'
    RARELITY = 'rarelity'
    SLOT = 'slot'
    INITIAL_STATUS = 'initial_status'
    MAX_STATUS = 'max_status'
    INITIAL_STATUS_TOKU = 'toku_initial_status'
    MAX_STATUS_TOKU = 'toku_max_status'
    UP = 'up'
    RANGE = 'range'
    TOKU_LEVEL = 'toku'
