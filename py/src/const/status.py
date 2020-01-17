# coding: utf-8

__all__ = ['Status']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from enum import Enum


class Status(Enum):
    LEVEL = 'レベル'
    HP_MAX = '生存'
    ATTACK = '打撃'
    DEFENSE = '統率'
    MOBILE = '機動'
    BACK = '衝力'
    SCOUT = '偵察'
    LOYALTIES = '必殺'
    HIDE = '隠蔽'
    KEY_LEVEL = 'level'
    KEY_HP_MAX = 'hp_max'
    KEY_ATTACK = 'attack'
    KEY_DEFENSE = 'defense'
    KEY_MOBILE = 'mobile'
    KEY_BACK = 'back'
    KEY_SCOUT = 'scout'
    KEY_LOYALTIES = 'loyalities'
    KEY_HIDE = 'hide'
