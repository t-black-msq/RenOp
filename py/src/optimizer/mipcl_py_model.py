# coding: utf-8

__all__ = ['RenketsuModel']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os
import mipcl_py.mipshell.mipshell as mp

import pandas

from const import Status, ToukenInfoKey
from utils import KatanaInfo


class RenketsuModel(mp.Problem):
    """"""

    weight = {1: 1, 2: 1, 3: 1, 4: 3, 5: 5}

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
    def attack(self):
        return self.__attack

    @property
    def defense(self):
        return self.__defense

    @property
    def mobile(self):
        return self.__mobile

    @property
    def back(self):
        return self.__back

    @property
    def target_status(self):
        return (
            Status.KEY_ATTACK.value,
            Status.KEY_DEFENSE.value,
            Status.KEY_MOBILE.value,
            Status.KEY_BACK.value)

    def add_renketsu_data(
            self,
            katana: KatanaInfo,
            level: int,
            attack: int,
            defense: int,
            mobile: int,
            back: int,
            possessed: pandas.core.frame.DataFrame):
        self.__katana = katana
        self.__level = level
        self.__attack = attack
        self.__defense = defense
        self.__mobile = mobile
        self.__back = back
        self.__possessed = possessed
        self.__has_data = True

    def set_toku(self):
        self.__toku = True

    def add_variable(self):
        self.__x = {}
        for uid in self.__all_data:
            num = self.__possessed.at[uid, '所持数']
            if num > 0:
                name = self.__all_data[uid][ToukenInfoKey.NAME.value].replace(
                    ' ', '_')
                # x_i \in \mathbb{N} \forall i \in K
                self.__x[uid] = mp.Var(name, mp.INT, ub=num)
        if len(self.__x) == 0:
            print('ERROR: 錬結で使用する刀剣を possessed.csv に入力してください')
            os._exit(1)
        # o \in \mathbb{N}
        self.__over = mp.Var(f'over')

    def set_objective(self, weightA: int = 10, weightB: int = 1):
        # \sum_{i \in K} 10 x_i + o
        mp.minimize(weightA *
                    mp.sum_(self.weight[self.__all_data[uid][ToukenInfoKey.RARELITY.value]] *
                            self.__x[uid] for uid in self.__x) +
                    weightB *
                    self.__over)

    def add_constraint(self):
        self.__set_over_constr()
        self.__set_status_constraint()

    def add_constraint2(self):
        self.__set_over_constr2()
        self.__set_status_constraint2()

    def __set_status_constraint(self):
        for status in self.target_status:
            mp.sum_(self.__all_data[uid][ToukenInfoKey.UP.value][status] * self.__x[uid]
                    for uid in self.__x) >= self.__katana[self.status][status] - getattr(self, status)

    def __set_status_constraint2(self):
        for status in self.target_status:
            mp.sum_(self.__all_data[uid][ToukenInfoKey.UP.value][status] * self.__x[uid]
                    for uid in self.__x) <= self.__katana[self.status][status] - getattr(self, status)

    def __set_over_constr(self):
        self.__over == mp.sum_(mp.sum_(self.__all_data[uid][ToukenInfoKey.UP.value][status] * self.__x[uid] for uid in self.__x) for status in self.target_status) - sum(
            self.__katana[self.status][status] for status in self.target_status) + self.__attack + self.__defense + self.__mobile + self.__back

    def __set_over_constr2(self):
        self.__over == mp.sum_(mp.sum_(self.__all_data[uid][ToukenInfoKey.UP.value][status] * self.__x[uid] for uid in self.__x) for status in self.target_status) + sum(
            self.__katana[self.status][status] for status in self.target_status) - self.__attack - self.__defense - self.__mobile - self.__back

    def make_problem(self, weightA: int = 10, weightB: int = 1):
        if self.__has_data:
            self.add_variable()
            self.set_objective(weightA, weightB)
            self.add_constraint()
        else:
            raise Exception(
                'call add_renketsu_data method before calling this')

    def make_problem2(self, weightA: int = 10, weightB: int = 1):
        if self.__has_data:
            self.add_variable()
            self.set_objective(weightA, weightB)
            self.add_constraint2()
        else:
            raise Exception(
                'call add_renketsu_data method before calling this')
