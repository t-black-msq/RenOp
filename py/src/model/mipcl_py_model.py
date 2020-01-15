# coding: utf-8

__all__ = ['RenketsuModel']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os
import mipcl_py.mipshell.mipshell as mp

import pandas

from utils import KatanaInfo


class RenketsuModel(mp.Problem):
    """"""

    def __init__(self, model_name: str, all_data: dict):
        super().__init__(model_name)
        self.__all_data = all_data
        self.__has_data = False
        self.__toku = False

    @property
    def x(self):
        return self.__x

    @property
    def over(self):
        return self.__over

    @property
    def status(self):
        return 'toku_max_status' if self.__toku else 'max_status'

    @property
    def dageki(self):
        return self.__dageki

    @property
    def tousotsu(self):
        return self.__tousotsu

    @property
    def kidou(self):
        return self.__kidou

    @property
    def shouryoku(self):
        return self.__shouryoku

    @property
    def target_status(self):
        return ('dageki', 'tousotsu', 'kidou', 'shouryoku')

    def add_renketsu_data(
            self,
            katana: KatanaInfo,
            level: int,
            dageki: int,
            tousotsu: int,
            kidou: int,
            shouryoku: int,
            possessed: pandas.core.frame.DataFrame):
        self.__katana = katana
        self.__level = level
        self.__dageki = dageki
        self.__tousotsu = tousotsu
        self.__kidou = kidou
        self.__shouryoku = shouryoku
        self.__possessed = possessed
        self.__has_data = True

    def set_toku(self):
        self.__toku = True

    def add_variable(self):
        self.__x = {}
        for uid in self.__all_data:
            num = self.__possessed.at[uid, '所持数']
            if num > 0:
                name = self.__all_data[uid]['display_name'].replace(' ', '_')
                # x_i \in \mathbb{N} \forall i \in K
                self.__x[uid] = mp.Var(f'x_{name}', mp.INT, ub=num)
        if len(self.__x) == 0:
            print('ERROR: 錬結で使用する刀剣を possessed.csv に入力してください')
            os._exit(1)
        # o \in \mathbb{N}
        self.__over = mp.Var(f'over')

    def set_objective(self):
        # \sum_{i \in K} 10 x_i + o
        mp.minimize(10 * mp.sum_(self.__x.values()) + self.__over)

    def add_constraint(self):
        self.__set_over_constr()
        self.__set_status_constraint()

    def __set_status_constraint(self):
        for status in self.target_status:
            mp.sum_(self.__all_data[uid]['up'][status] * self.__x[uid]
                    for uid in self.__x) >= self.__katana[self.status][status] - getattr(self, status)

    def __set_over_constr(self):
        self.__over == mp.sum_(mp.sum_(self.__all_data[uid]['up'][status] * self.__x[uid] for uid in self.__x) for status in self.target_status) - sum(
            self.__katana[self.status][status] for status in self.target_status) + self.__dageki + self.__tousotsu + self.__kidou + self.__shouryoku

    def make_problem(self):
        if self.__has_data:
            self.add_variable()
            self.set_objective()
            self.add_constraint()
        else:
            raise Exception(
                'call add_renketsu_data method before calling this')
