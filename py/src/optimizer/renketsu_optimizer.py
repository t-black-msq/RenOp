# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os

from data import DataAccessor
from model import Touken
from .mipcl_py_model import RenketsuModel

from const import HIGEKIRI, HIZAMARU, SEPARATOR, Status, ToukenInfoKey
from utils import is_integer, read_avant, read_possessed, reflect_to_possessed, write_avant, write_possessed


class RenketsuOptimizer:

    __MAIN_MESSAGE = (
        '錬結する刀剣の情報を入力してください\n'
        ' ※ 数値は半角のみ\n'
        ' ※ 中断する場合は q')
    __SAME_MESSAGE = ' ※ 前回と同じ条件の場合は s'
    __DATA_MESSAGE = ' ※ data.json から possessed.csv を読み直す場合は data'
    __MAX_MESSAGE = ' ※ 所持刀剣数を 999 で試す場合は max\n 　 (極を除外する場合は max2)'
    __NO_OR_NAME = '■ 刀帳No または 刀剣名: '
    __RETRY_MESSAGE = 'もう一度入力してください'

    def __init__(self):
        self.__accessor = DataAccessor()
        self.__all = self.__accessor.get_all()
        self.__model = RenketsuModel('renketsu', self.__all)
        self.__possessed = read_possessed()
        self.__data = None
        self.__mode = 0
        self.__infeasible = False
        self.__output = False

    def set_initial_data(self):
        self.__set_touken_from_avant()
        self.__model.add_renketsu_data(self.__touken, self.__possessed)

    def input_renketsu_touken(self):
        if self.__data:
            return

        print('\n'.join([self.__MAIN_MESSAGE, self.__SAME_MESSAGE,
                         self.__DATA_MESSAGE, self.__MAX_MESSAGE, SEPARATOR]))
        self.__input_touken()
        self.__input_status()
        write_avant(self.__touken.make_avant_message(self.__mode))

        self.__model.add_renketsu_data(self.__touken, self.__possessed)

    def __input_touken(self):
        identifier = input(self.__NO_OR_NAME)
        self.__touken_info = self.__accessor.get_katana(identifier)
        while self.__touken_info is None:
            if identifier == 'q':
                os._exit(1)
            elif identifier == 's':
                self.__set_touken_from_avant()
                return
            elif identifier in ('max', 'max2'):
                self.__mode = 1 if identifier == 'max' else 2
                self.__maximize_possessed()
                print('--- max mode ---')
                print('\n'.join([self.__MAIN_MESSAGE, self.__SAME_MESSAGE]))
            else:
                if identifier == 'data':
                    reflect_to_possessed()
                print(self.__RETRY_MESSAGE)
            identifier = input(self.__NO_OR_NAME)
            self.__touken_info = self.__accessor.get_katana(identifier)
        self.__touken = Touken(self.__accessor.get_katana(identifier))
        self.__input_level()
        self.__touken.parse_info()

    def __input_level(self):
        message = f'■ {Status.LEVEL.value}: '
        val = input(message)
        while True:
            try:
                if val == 'q':
                    os._exit(1)
                if self.__touken.set_level(int(val)):
                    break
            except BaseException:
                print(self.__RETRY_MESSAGE)
                val = input(message)

    def __input_status(self):
        if self.__data:
            return

        self.__input_integer(Status.ATTACK)
        self.__input_integer(Status.DEFENSE)
        self.__input_integer(Status.MOBILE)
        self.__input_integer(Status.BACK)

    def __input_integer(self, status: Status):
        message = f'■ {status.value}: '
        val = input(message)
        while True:
            try:
                if val == 'q':
                    os._exit(1)
                if self.__touken.set_status(status, int(val)):
                    break
            except BaseException:
                print(self.__RETRY_MESSAGE)
                val = input(message)

    def __set_touken_from_avant(self):
        data = read_avant()
        self.__data = data
        self.__mode = int(data[17])

        self.__touken = Touken(
            self.__accessor.get_katana(data[:3]), int(data[3:5]))
        self.__touken.set_status(Status.ATTACK, int(data[5:8]))
        self.__touken.set_status(Status.DEFENSE, int(data[8:11]))
        self.__touken.set_status(Status.MOBILE, int(data[11:14]))
        self.__touken.set_status(Status.BACK, int(data[14:17]))

    def __maximize_possessed(self):
        for idx in self.__possessed.index:
            if self.__possessed.at[idx, '刀名'].endswith(' 極'):
                if self.__mode == 2:
                    continue
            self.__possessed.at[idx, '所持数'] = 999

    def make_problem(self, weightA: int = 10, weightB: int = 1):
        self.__model.make_problem(weightA, weightB)

    def make_problem2(self, weightA: int = 10, weightB: int = 1):
        self.__model.make_problem2(weightA, weightB)

    def optimize(self):
        self.__model.optimize()

    def print_solution(self):
        if self.__model.is_solution:
            if self.__model.getObjVal() > 1e-5:
                print(f' cost: {self.__model.getObjVal()}')
                for uid in self.__model.x:
                    var = self.__model.x[uid]
                    if var.val > 1e-5:
                        print(f'  {uid} {var.name}: {int(var.val):>2d}')
                print(f'  余剰: {int(self.__model.over.val)}')
        elif self.__model.is_infeasible:
            print('NOT FOUND: ステータスをMAXにできません')
            self.__infeasible = True

    def write_possessed(self, id_: str):
        for uid in self.__possessed.index:
            if uid in self.__model.x:
                self.__possessed.at[uid, '所持数'] = (
                    self.__possessed.at[uid, '所持数'] - self.__model.x[uid].val)

        write_possessed(self.__possessed, id_)
        self.__output = True

    def use_all(self):
        print('所持している刀剣をすべて使うと')
        up_attack = 0
        up_defense = 0
        up_mobile = 0
        up_back = 0
        for idx in self.__possessed.query('所持数 > 0').index:
            up_attack += self.__possessed.at[idx, '所持数'] * \
                self.__all[idx]['up'][Status.KEY_ATTACK.value]
            up_defense += self.__possessed.at[idx, '所持数'] * \
                self.__all[idx]['up'][Status.KEY_DEFENSE.value]
            up_mobile += self.__possessed.at[idx, '所持数'] * \
                self.__all[idx]['up'][Status.KEY_MOBILE.value]
            up_back += self.__possessed.at[idx, '所持数'] * \
                self.__all[idx]['up'][Status.KEY_BACK.value]
        max_attack = self.__touken.max_status[Status.KEY_ATTACK.value]
        max_defense = self.__touken.max_status[Status.KEY_DEFENSE.value]
        max_mobile = self.__touken.max_status[Status.KEY_MOBILE.value]
        max_back = self.__touken.max_status[Status.KEY_BACK.value]
        print(
            f'■ {Status.ATTACK.value}: {self.__touken.attack:3d} --> {min(self.__touken.attack + up_attack, max_attack):3d} (MAX: {max_attack:3d})')
        print(
            f'■ {Status.DEFENSE.value}: {self.__touken.defense:3d} --> {min(self.__touken.defense + up_defense, max_defense):3d} (MAX: {max_defense:3d})')
        print(
            f'■ {Status.MOBILE.value}: {self.__touken.mobile:3d} --> {min(self.__touken.mobile + up_mobile, max_mobile):3d} (MAX: {max_mobile:3d})')
        print(
            f'■ {Status.BACK.value}: {self.__touken.back:3d} --> {min(self.__touken.back + up_back, max_back):3d} (MAX: {max_back:3d})')

    @property
    def is_infeasible(self) -> bool:
        return self.__infeasible

    @property
    def output(self) -> bool:
        return self.__output

    @property
    def is_max(self) -> bool:
        return self.__mode > 0
