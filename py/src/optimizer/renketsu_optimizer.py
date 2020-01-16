# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import csv
import os

from data import DataAccessor
from model import Touken
from .mipcl_py_model import RenketsuModel

from utils import is_integer, read_avant, read_possessed, write_avant


class RenketsuOptimizer(object):
    """"""

    status_map = {
        'dageki': '打撃',
        'tousotsu': '統率',
        'kidou': '機動',
        'shouryoku': '衝力',
        'level': 'レベル'}

    def __init__(self, data: str = None):
        self.__accessor = DataAccessor()
        self.__katana = None
        self.__all = self.__accessor.get_all()
        self.__model = RenketsuModel('renketsu', self.__all)
        self.__possessed = read_possessed()
        self.__inputted = False
        self.__toku = False
        self.__given_data = data is not None

    @property
    def katana(self):
        return self.__katana

    @property
    def model(self):
        return self.__model

    def add_objective(self):
        if self.__given_data:
            self.__inputted = True
        else:
            print('錬結する刀剣の情報を入力してください')
            print(' ※ 数値は半角のみ')
            print(' ※ 中断する場合は q')
            print(' ※ 前回と同じ条件の場合は s')
            print('-------------------------------------------------------')
            self.__make_user_input_katana()

        if self.__inputted:
            self.parse_avant(read_avant())
        else:
            self.__level = self.__make_user_input_integer('level')
            self.check_level()
            self.__dageki = self.__make_user_input_integer('dageki')
            self.__tousotsu = self.__make_user_input_integer('tousotsu')
            self.__kidou = self.__make_user_input_integer('kidou')
            self.__shouryoku = self.__make_user_input_integer('shouryoku')

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
            print('もう一度入力してください')
            identifier = input('刀帳No または 刀剣名: ')
        self.__katana = k

    def __make_user_input_integer(self, status_name: str) -> int:
        message = f'■ {self.status_map[status_name]}: '
        val = input(message)
        while not is_integer(val) or not self.check_param(
                status_name, int(val)):
            if val == 'q':
                os._exit(1)
            print('もう一度入力してください')
            val = input(message)
        return int(val)

    def check_level(self):
        if self.__katana['name'].startswith('Higekiri'):
            for uid in ('107', '108', '109', '110'):
                if self.__level < self.__all[uid]['toku']:
                    self.__katana = self.__all[uid]
        elif self.__katana['name'].startswith('Hizamaru'):
            for uid in ('112', '113', '114'):
                if self.__level < self.__all[uid]['toku']:
                    self.__katana = self.__all[uid]
        elif self.__katana['toku'] <= self.__level:
            self.__model.set_toku()
            self.__toku = True

    def check_param(self, name: str, val: int) -> bool:
        if name == 'level':
            return True
        elif self.__level < self.__katana['toku']:
            if val < self.__katana['initial_status'][name]:
                print(f'入力された {self.status_map[name]} が初期ステータスより低いです')
            elif self.__katana['max_status'][name] < val:
                print(f'入力された {self.status_map[name]} が最大ステータスより高いです')
            else:
                return True
        else:
            if val < self.__katana['toku_initial_status'][name]:
                print(f'入力された {self.status_map[name]} が初期ステータスより低いです')
            elif self.__katana['toku_max_status'][name] < val:
                print(f'入力された {self.status_map[name]} が最大ステータスより高いです')
            else:
                return True
        return False

    def make_problem(self, weightA: int = 10, weightB: int = 1):
        self.__model.make_problem(weightA, weightB)

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

    def write_possessed(self):
        for uid in self.__possessed.index:
            if uid in self.__model.x:
                self.__possessed.at[uid, '所持数'] = (
                    self.__possessed.at[uid, '所持数'] - self.__model.x[uid].val)

        self.__possessed.to_csv(
            '../../possessed_new.csv',
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding='cp932')

    def parse_avant(self, data: str):
        Touken(no=data[:3])
        self.__katana = self.__accessor.get_katana(data[:3])
        self.__level = int(data[3:5])
        self.__dageki = int(data[5:8])
        self.__tousotsu = int(data[8:11])
        self.__kidou = int(data[11:14])
        self.__shouryoku = int(data[14:17])
        self.check_level()

        if not self.__given_data:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f'■ 刀帳No: {self.__katana["uid"]}')
            print(
                f'■ 刀剣名: {self.__katana["display_name"]}{" 特" if self.__toku else ""}')
            print(f'■ {self.status_map["level"]}: {self.__level}')
            print(f'■ {self.status_map["dageki"]}: {self.__dageki}')
            print(f'■ {self.status_map["tousotsu"]}: {self.__tousotsu}')
            print(f'■ {self.status_map["kidou"]}: {self.__kidou}')
            print(f'■ {self.status_map["shouryoku"]}: {self.__shouryoku}')

    def compile_avant(self):
        return f'{self.__katana["uid"]}{self.__level:02d}{self.__dageki:03d}{self.__tousotsu:03d}{self.__kidou:03d}{self.__shouryoku:03d}'
