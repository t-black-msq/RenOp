# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os

from data import DataAccessor
from model import RenketsuModel

from utils import is_integer, read_possessed


class RenketsuOptimizer(object):
    """"""

    status_map = {
        'dageki': '打撃',
        'tousotsu': '統率',
        'kidou': '機動',
        'shouryoku': '衝力',
        'level': 'レベル'}

    def __init__(self):
        self.__accessor = DataAccessor()
        self.__katana = None
        self.__all = self.__accessor.get_all()
        self.__model = RenketsuModel('renketsu', self.__all)
        self.__possessed = read_possessed()

    @property
    def katana(self):
        return self.__katana

    @property
    def model(self):
        return self.__model

    def add_objective(self):
        print('---------------------------------------------')
        print('錬結する刀剣の情報を入力してください')
        print(' ※ 数値は半角のみ')
        print(' ※ 中断する場合は q')
        print('---------------------------------------------')
        self.__make_user_input_katana()

        self.__level = self.__make_user_input_integer('level')
        self.check_level()
        self.__dageki = self.__make_user_input_integer('dageki')
        self.__tousotsu = self.__make_user_input_integer('tousotsu')
        self.__kidou = self.__make_user_input_integer('kidou')
        self.__shouryoku = self.__make_user_input_integer('shouryoku')

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

    def make_problem(self):
        self.__model.make_problem()

    def optimize(self):
        self.print_model()
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

    def print_(self):
        if self.__model.is_solution:
            print('--- solution ---')
            self.__model.printSolution()
            # print(self.__model.getObjVal())
            # for uid in self.__model.x:
            #     print(f'{uid}: {self.__model.x[uid].val}')
            # print(self.__model.over.val)
        elif self.__model.is_infeasible:
            print('NOT FOUND: ステータスをMAXにできません')
