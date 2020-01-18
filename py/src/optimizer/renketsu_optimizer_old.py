# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os

from data import DataAccessor
from model import Touken
from .mipcl_py_model import RenketsuModel

from const import HIGEKIRI, HIZAMARU, Status, ToukenInfoKey
from utils import is_integer, read_avant, read_possessed, reflect_to_possessed, write_avant, write_possessed


class RenketsuOptimizer(object):
    """"""

    status_map = {
        Status.KEY_ATTACK: Status.ATTACK.value,
        Status.KEY_DEFENSE: Status.DEFENSE.value,
        Status.KEY_MOBILE: Status.MOBILE.value,
        Status.KEY_BACK: Status.BACK.value,
        Status.KEY_LEVEL: Status.LEVEL.value}

    def __init__(self, data: str = None):
        self.__accessor = DataAccessor()
        self.__katana = None
        self.__all = self.__accessor.get_all()
        self.__model = RenketsuModel('renketsu', self.__all)
        self.__possessed = read_possessed()
        self.__inputted = False
        self.__toku = False
        self.__max = False
        self.__infeasible = False
        self.__max_no_kiwami = False
        self.__output = False
        self.__given_data = data is not None
        self.__mode = 0

    @property
    def katana(self):
        return self.__katana

    @property
    def model(self):
        return self.__model

    @property
    def is_infeasible(self) -> bool:
        return self.__infeasible

    @property
    def output(self) -> bool:
        return self.__output

    @property
    def is_max(self) -> bool:
        return self.__mode > 0

    def add_objective(self):
        if self.__given_data:
            self.__inputted = True
        else:
            print('錬結する刀剣の情報を入力してください')
            print(' ※ 数値は半角のみ')
            print(' ※ 中断する場合は q')
            print(' ※ 前回と同じ条件の場合は s')
            print(' ※ data.json から possessed.csv を読み直す場合は data')
            print(' ※ 所持刀剣数を 999 で試す場合は max')
            print(' 　 (極を除外する場合は max2)')
            print('------------------------------------------------------------')
            self.__make_user_input_katana()

        if self.__inputted:
            self.parse_avant(read_avant())
        else:
            self.__level = self.__make_user_input_integer(Status.KEY_LEVEL)
            self.check_level()
            self.__dageki = self.__make_user_input_integer(Status.KEY_ATTACK)
            self.__tousotsu = self.__make_user_input_integer(
                Status.KEY_DEFENSE)
            self.__kidou = self.__make_user_input_integer(Status.KEY_MOBILE)
            self.__shouryoku = self.__make_user_input_integer(Status.KEY_BACK)

        if self.__mode > 0:
            self.__maximize_possessed()

        write_avant(self.compile_avant())

        self.__model.add_renketsu_data(
            self.__katana,
            self.__level,
            self.__dageki,
            self.__tousotsu,
            self.__kidou,
            self.__shouryoku,
            self.__possessed)

    def __make_user_input_katana(self):
        identifier = input('■ 刀帳No または 刀剣名: ')
        k = self.__accessor.get_katana(identifier)
        while k is None:
            if identifier == 'q':
                os._exit(1)
            elif identifier == 's':
                self.__inputted = True
                return
            elif identifier in ('max', 'max2'):
                if identifier == 'max':
                    self.__mode = 1
                else:
                    self.__mode = 2
                print('-- max mode --')
                print('錬結する刀剣の情報を入力してください')
                print(' ※ 数値は半角のみ')
                print(' ※ 中断する場合は q')
                print(' ※ 前回と同じ条件の場合は s')
            elif identifier == 'data':
                reflect_to_possessed()
            else:
                print('もう一度入力してください')
            identifier = input('刀帳No または 刀剣名: ')
            k = self.__accessor.get_katana(identifier)
        self.__katana = k

    def __make_user_input_integer(self, status: Status) -> int:
        message = f'■ {self.status_map[status]}: '
        val = input(message)
        while not is_integer(val) or not self.check_param(status, int(val)):
            if val == 'q':
                os._exit(1)
            print('もう一度入力してください')
            val = input(message)
        return int(val)

    def check_level(self):
        if self.__katana[ToukenInfoKey.NAME_EN.value].startswith('Higekiri'):
            for uid in HIGEKIRI:
                if self.__level < self.__all[uid][ToukenInfoKey.TOKU_LEVEL.value]:
                    self.__katana = self.__all[uid]
        elif self.__katana[ToukenInfoKey.NAME_EN.value].startswith('Hizamaru'):
            for uid in HIZAMARU:
                if self.__level < self.__all[uid][ToukenInfoKey.TOKU_LEVEL.value]:
                    self.__katana = self.__all[uid]
        elif self.__katana[ToukenInfoKey.TOKU_LEVEL.value] <= self.__level:
            self.__model.set_toku()
            self.__toku = True

    def check_param(self, status: Status, val: int) -> bool:
        if status is Status.KEY_LEVEL:
            return True
        elif self.__level < self.__katana[ToukenInfoKey.TOKU_LEVEL.value]:
            if val < self.__katana['initial_status'][status.value]:
                print(f'入力された {self.status_map[status]} が初期ステータスより低いです')
            elif self.__katana['max_status'][status.value] < val:
                print(f'入力された {self.status_map[status]} が最大ステータスより高いです')
            else:
                return True
        else:
            if val < self.__katana['toku_initial_status'][status.value]:
                print(f'入力された {self.status_map[status]} が初期ステータスより低いです')
            elif self.__katana['toku_max_status'][status.value] < val:
                print(f'入力された {self.status_map[status]} が最大ステータスより高いです')
            else:
                return True
        return False

    def make_problem(self, weightA: int = 10, weightB: int = 1):
        self.__model.make_problem(weightA, weightB)

    def make_problem2(self, weightA: int = 10, weightB: int = 1):
        self.__model.make_problem2(weightA, weightB)

    def optimize(self):
        self.__model.optimize()

    def print_model(self):
        print('--- variables ---')
        for v in self.__model.vars:
            print(v)
        print('--- objective ---')
        print(self.__model.obj)
        print('--- constraints ---')
        for c in self.__model.ctrs:
            print(c)

    def print_(self, print_model: bool = True):
        if print_model:
            print_model()
        if self.__model.is_solution:
            print(f' cost: {self.__model.getObjVal()}')
            for uid in self.__model.x:
                if self.__model.x[uid].val > 1e-5:
                    print(
                        f'  {uid} {self.__model.x[uid].name}: {int(self.__model.x[uid].val):>2d}')
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

    def parse_avant(self, data: str):
        self.__katana = self.__accessor.get_katana(data[:3])
        t = Touken(self.__accessor.get_katana(data[:3]), int(data[3:5]))
        self.__level = int(data[3:5])
        self.__dageki = int(data[5:8])
        t.set_status(Status.ATTACK, int(data[5:8]))
        self.__tousotsu = int(data[8:11])
        t.set_status(Status.DEFENSE, int(data[8:11]))
        self.__kidou = int(data[11:14])
        t.set_status(Status.MOBILE, int(data[11:14]))
        self.__shouryoku = int(data[14:17])
        t.set_status(Status.BACK, int(data[14:17]))
        if self.__mode == 0:
            self.__mode = int(data[17])
        self.check_level()
        self.t = t

        if not self.__given_data:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(t)

    def compile_avant(self):
        return f'{self.__katana["uid"]}{self.__level:02d}{self.__dageki:03d}{self.__tousotsu:03d}{self.__kidou:03d}{self.__shouryoku:03d}{self.__mode}'

    def __maximize_possessed(self):
        for idx in self.__possessed.index:
            if self.__possessed.at[idx, '刀名'].endswith(' 極'):
                if self.__mode == 2:
                    continue
            self.__possessed.at[idx, '所持数'] = 999

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
        max_attack = self.t.max_status[Status.KEY_ATTACK.value]
        max_defense = self.t.max_status[Status.KEY_DEFENSE.value]
        max_mobile = self.t.max_status[Status.KEY_MOBILE.value]
        max_back = self.t.max_status[Status.KEY_BACK.value]
        print(
            f'■ {Status.ATTACK.value}: {self.__dageki:3d} --> {min(self.__dageki + up_attack, max_attack):3d} (MAX: {max_attack:3d})')
        print(
            f'■ {Status.DEFENSE.value}: {self.__tousotsu:3d} --> {min(self.__tousotsu + up_defense, max_defense):3d} (MAX: {max_defense:3d})')
        print(
            f'■ {Status.MOBILE.value}: {self.__kidou:3d} --> {min(self.__kidou + up_mobile, max_mobile):3d} (MAX: {max_mobile:3d})')
        print(
            f'■ {Status.BACK.value}: {self.__shouryoku:3d} --> {min(self.__shouryoku + up_back, max_back):3d} (MAX: {max_back:3d})')
