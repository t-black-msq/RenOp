# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from data import DataAccessor
from model import RenketsuModel

from utils import is_integer, read_possessed


class RenketsuOptimizer(object):
    """"""

    def __init__(self):
        self.__accessor = DataAccessor()
        self.__katana = None
        self.__model = RenketsuModel('renketsu')
        self.__possessed = read_possessed()

    @property
    def katana(self):
        return self.__katana

    def add_objective(self):
        identifier = input('Input Katana No or Katana Name: ')
        if identifier:
            self.__katana = self.__accessor.get_katana(identifier)
        else:
            print('invalid')

        if self.__katana is None:
            print('no katana')
            return

        print(f'Input {self.__katana["display_name"]}\'s recent status value')
        self.__dageki = self.__make_user_input_integer('Dageki: ')
        self.__tousotsu = self.__make_user_input_integer('Tousotsu: ')
        self.__kidou = self.__make_user_input_integer('Kidou: ')
        self.__shouryoku = self.__make_user_input_integer('Shouryoku: ')

    def __make_user_input_integer(self, message: str) -> int:
        val = input(message)
        while (not is_integer(val)):
            val = input(message)
        return int(val)

    def optimize(self):
        ...
