# coding: utf-8

__all__ = ['Touken']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from data import DataAccessor


class Touken(object):

    accessor = DataAccessor()

    def __init__(self, *, no: str = None, name: str = None):
        if no:
            self.__get_info_by_no(no)
        elif name:
            self.__get_info_by_name(name)
        else:
            raise ValueError()

        self.__parse_info()

    def __get_info_by_no(self, no: str):
        if len(no) != 3:
            no = f'{int(no):03d}'
        self.__info = self.accessor.get_katana(no)

    def __get_info_by_name(self, name: str):
        self.__info = self.accessor.get_katana(no)

    def __parse_info(self):
        ...
