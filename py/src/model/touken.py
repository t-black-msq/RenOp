# coding: utf-8

__all__ = ['Touken']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from typing import Any, Dict, Tuple

from const import HIGEKIRI, HIZAMARU, TOKU, Status, ToukenInfoKey
from data import DataAccessor
from utils import KatanaInfo


class ToukenStatus(object):

    __LG_MESSAGE = '入力された {0} が初期ステータスより{1}です'
    __LOWER = '低い'
    __GREATER = '高い'

    def __init__(self):
        self.__level = None
        self.__hp_max = None
        self.__attack = None
        self.__defense = None
        self.__mobile = None
        self.__back = None
        self.__scout = None
        self.__loyalties = None
        self.__hide = None

    def set_all_status(
            self,
            hp_max: int,
            attack: int,
            defense: int,
            mobile: int,
            back: int,
            scout: int,
            loyalties: int,
            hide: int):
        if self.__level:
            self.__hp_max = hp_max
            self.__attack = attack
            self.__defense = defense
            self.__mobile = mobile
            self.__back = back
            self.__scout = scout
            self.__loyalties = loyalties
            self.__hide = hide
        else:
            print('Set level before setting other status')

    def set_status(self, status: Status, value: int) -> bool:
        valid = False
        if self.__level:
            if status is Status.HP_MAX:
                if self.__check_level(value):
                    self.__hp_max = value
                    valid = True
            elif status is Status.ATTACK:
                if self.__check_status(
                        Status.ATTACK, Status.KEY_ATTACK, value):
                    self.__attack = value
                    valid = True
            elif status is Status.DEFENSE:
                if self.__check_status(
                        Status.DEFENSE, Status.KEY_DEFENSE, value):
                    self.__defense = value
                    valid = True
            elif status is Status.MOBILE:
                if self.__check_status(
                        Status.MOBILE, Status.KEY_MOBILE, value):
                    self.__mobile = value
                    valid = True
            elif status is Status.BACK:
                if self.__check_status(
                        Status.BACK, Status.KEY_BACK, value):
                    self.__back = value
                    valid = True
            elif status is Status.SCOUT:
                if self.__check_status(
                        Status.SCOUT, Status.KEY_SCOUT, value):
                    self.__scout = value
                    valid = True
            elif status is Status.LOYALTIES:
                self.__loyalties = self.__status_i[Status.KEY_LOYALTIES.value]
                valid = True
            elif status is Status.HIDE:
                if self.__check_status(
                        Status.HIDE, Status.KEY_HIDE, value):
                    self.__hide = value
                    valid = True
        else:
            print('Set level before setting other status')
        return valid

    def set_level(self, level: int):
        if self.__check_level(level):
            self.__level = level
            return True
        return False

    def set_limit_status(self, initial: Dict[str, int], max_: Dict[str, int]):
        self.__status_i = initial
        self.__status_m = max_

    def __check_level(self, level: int) -> bool:
        if level < 1:
            print(self.__LG_MESSAGE.format(Status.LEVEL.value, self.__LOWER))
        elif 99 < level:
            print(self.__LG_MESSAGE.format(Status.LEVEL.value, self.__GREATER))
        return 1 <= level <= 99

    def __check_status(self, status: Status, key: Status, val: int) -> bool:
        if val < self.__status_i[key.value]:
            print(self.__LG_MESSAGE.format(Status.value, self.__LOWER))
        elif self.__status_m[key.value] < val:
            print(self.__LG_MESSAGE.format(Status.value, self.__GREATER))
        return self.__status_i[key.value] <= val <= self.__status_m[key.value]

    @property
    def level(self) -> int:
        return self.__level

    @property
    def hp_max(self) -> int:
        """生存"""
        return self.__hp_max

    @property
    def attack(self) -> int:
        """打撃"""
        return self.__attack

    @property
    def defense(self) -> int:
        """統率"""
        return self.__defense

    @property
    def mobile(self) -> int:
        """機動"""
        return self.__mobile

    @property
    def back(self) -> int:
        """衝力"""
        return self.__back

    @property
    def scout(self) -> int:
        """偵察"""
        return self.__scout

    @property
    def loyalties(self) -> int:
        """必殺"""
        return self.__loyalties

    @property
    def hide(self) -> int:
        """隠蔽"""
        return self.__hide


class Touken(ToukenStatus):

    accessor = DataAccessor()

    def __init__(self, info: KatanaInfo, level: int = None):
        super().__init__()

        self.__info = info
        if level:
            self.set_level(level)
            self.parse_info()

    def __str__(self) -> str:
        return '\n'.join([f'■ 刀帳No: {self.__uid}',
                          f'■ 刀剣名: {self.__name}{" 特" if self.is_toku else ""}',
                          f'■ {Status.LEVEL.value}: {self.level}',
                          f'■ {Status.ATTACK.value}: {self.attack}',
                          f'■ {Status.DEFENSE.value}: {self.defense}',
                          f'■ {Status.MOBILE.value}: {self.mobile}',
                          f'■ {Status.BACK.value}: {self.back}'])

    def parse_info(self):
        self.__uid = self.__info[ToukenInfoKey.UID.value]
        self.__name = self.__info[ToukenInfoKey.NAME.value]
        self.__toku_level = self.__info[ToukenInfoKey.TOKU_LEVEL.value]

        if self.__check_toku():
            self.__initial_status = self.__info[ToukenInfoKey.INITIAL_STATUS_TOKU.value]
            self.__max_status = self.__info[ToukenInfoKey.MAX_STATUS_TOKU.value]
        else:
            self.__initial_status = self.__info[ToukenInfoKey.INITIAL_STATUS.value]
            self.__max_status = self.__info[ToukenInfoKey.MAX_STATUS.value]

        self.__faction = self.__info[ToukenInfoKey.FACTION.value]
        self.__kind = self.__info[ToukenInfoKey.KIND.value]
        self.__range = self.__info[ToukenInfoKey.RANGE.value]
        self.__rarelity = self.__info[ToukenInfoKey.RARELITY.value]
        self.__slot = self.__info[ToukenInfoKey.SLOT.value]

        self.set_limit_status(self.__initial_status, self.__max_status)

    def __check_toku(self) -> bool:
        if self.__uid in HIGEKIRI + HIZAMARU:
            return self.__check_genji_brothers()
        return self.__toku_level <= self.level

    def __check_genji_brothers(self):
        if self.__uid in HIGEKIRI:
            for uid in HIGEKIRI:
                tmp = self.accessor.get_katana(uid)
                if self.level < tmp[ToukenInfoKey.TOKU_LEVEL.value]:
                    if self.__uid != uid:
                        self.__uid = uid
                        self.__name = tmp[ToukenInfoKey.NAME.value]
                        self.__toku_level = tmp[ToukenInfoKey.TOKU_LEVEL.value]
                        return False
                else:
                    continue
        elif self.__uid in HIZAMARU:
            for uid in HIZAMARU:
                tmp = self.accessor.get_katana(uid)
                if self.level < tmp[ToukenInfoKey.TOKU_LEVEL.value]:
                    if self.__uid != uid:
                        self.__uid = uid
                        self.__name = tmp[ToukenInfoKey.NAME.value]
                        self.__toku_level = tmp[ToukenInfoKey.TOKU_LEVEL.value]
                        return False
                else:
                    continue
        return False

    def make_avant_message(self, mode: int) -> str:
        return ''.join([self.__uid,
                        f'{self.level:02d}',
                        f'{self.attack:03d}',
                        f'{self.defense:03d}',
                        f'{self.mobile:03d}',
                        f'{self.back:03d}',
                        str(mode)])

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def name(self) -> str:
        return self.__name

    @property
    def toku_level(self) -> int:
        return self.__toku_level

    @property
    def rarelity(self) -> int:
        return self.__rarelity

    @property
    def initial_status(self) -> Dict[str, int]:
        return self.__initial_status

    @property
    def max_status(self) -> Dict[str, int]:
        return self.__max_status

    @property
    def is_toku(self) -> bool:
        return self.__toku_level <= self.level
