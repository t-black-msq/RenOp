# coding: utf-8

__all__ = ['Touken']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from typing import Any

from const import HIGEKIRI, HIZAMARU, TOKU, Status, ToukenInfoKey
from data import DataAccessor
from utils import KatanaInfo


class ToukenStatus(object):

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

    def set_status(self, status: Status, value: int):
        if self.__level:
            if status is Status.HP_MAX:
                self.__hp_max = value
            elif status is Status.ATTACK:
                self.__attack = value
            elif status is Status.DEFENSE:
                self.__defense = value
            elif status is Status.MOBILE:
                self.__mobile = value
            elif status is Status.BACK:
                self.__back = value
            elif status is Status.SCOUT:
                self.__scout = value
            elif status is Status.LOYALTIES:
                self.__loyalties = value
            elif status is Status.HIDE:
                self.__hide = value
        else:
            print('Set level before setting other status')

    def set_level(self, level: int):
        self.__level = level
        self.__check_level()

    def __check_level(self):
        self.__check_integer(self.__level, Status.KEY_LEVEL.value)
        if self.__level < 1 or 99 < self.__level:
            raise ValueError('invalid level value')

    def __check_loyalties(self):
        self.__check_integer(self.__loyalties, Status.KEY_LOYALTIES.value)

    def __check_integer(self, value: Any, name: str):
        if not isinstance(value, int):
            raise TypeError(f'{name} value must be integer')

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

    def __init__(self, info: KatanaInfo, level: int):
        super().__init__()

        self.set_level(level)
        self.__parse_info(info)

    def __str__(self) -> str:
        return '\n'.join([f'■ 刀帳No: {self.__uid}',
                          f'■ 刀剣名: {self.__name}',
                          f'■ {Status.LEVEL.value}: {self.level}',
                          f'■ {Status.ATTACK.value}: {self.attack}',
                          f'■ {Status.DEFENSE.value}: {self.defense}',
                          f'■ {Status.MOBILE.value}: {self.mobile}',
                          f'■ {Status.BACK.value}: {self.back}'])

    def __parse_info(self, info_dict: KatanaInfo):
        self.__uid = info_dict[ToukenInfoKey.UID.value]
        self.__name = info_dict[ToukenInfoKey.NAME.value]
        self.__toku_level = info_dict[ToukenInfoKey.TOKU_LEVEL.value]

        if self.__check_toku():
            self.__initial_status = info_dict[ToukenInfoKey.INITIAL_STATUS_TOKU.value]
            self.__max_status = info_dict[ToukenInfoKey.MAX_STATUS_TOKU.value]
        else:
            self.__initial_status = info_dict[ToukenInfoKey.INITIAL_STATUS.value]
            self.__max_status = info_dict[ToukenInfoKey.MAX_STATUS.value]

        self.__faction = info_dict[ToukenInfoKey.FACTION.value]
        self.__kind = info_dict[ToukenInfoKey.KIND.value]
        self.__range = info_dict[ToukenInfoKey.RANGE.value]
        self.__rarelity = info_dict[ToukenInfoKey.RARELITY.value]
        self.__slot = info_dict[ToukenInfoKey.SLOT.value]

    def __check_toku(self) -> bool:
        if HIGEKIRI + HIZAMARU:
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

    def make_avant_message(self, mode: str) -> str:
        return ''.join([self.__uid,
                        f'{self.level:02d}',
                        f'{self.attack:03d}',
                        f'{self.defense:03d}',
                        f'{self.mobile:03d}',
                        f'{self.back:03d}',
                        mode])

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_toku(self) -> bool:
        return self.__toku_level <= self.level

    @property
    def max_status(self) -> dict:
        return self.__max_status
