# coding: utf-8

__all__ = ['RenketsuOptimizer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from accessor import DataAccessor
from model import RenketsuModel


class RenketsuOptimizer(object):
    """"""

    def __init__(self):
        self.__accessor = DataAccessor()
        self.__katana = None
        self.__model = RenketsuModel('renketsu')

    @property
    def katana(self):
        return self.__katana

    def add_objective(self):
        identifier = input('Input Katana No or Katana Name')
        self.__katana = self.__accessor.get_katana(identifier)

        if self.__katana is None:
            ...

    def optimize(self):
        ...
