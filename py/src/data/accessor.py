# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from typing import List, Tuple

from utils import KatanaInfo, is_integer, read_data


class DataAccessor(object):
    """"""

    def __init__(self):
        self.__data = read_data()

    def get_katana(self, no_or_name: str) -> KatanaInfo:
        if is_integer(no_or_name):
            return self.__get_katana_by_no(no_or_name)
        return self.__get_katana_by_name(no_or_name)

    def __get_katana_by_no(self, no: str) -> KatanaInfo:
        return self.__data.get(f'{int(no):03d}')

    def __get_katana_by_name(self, name: str) -> KatanaInfo:
        candidates = self.__search_katana(name)
        if len(candidates) == 0:
            return None
        elif len(candidates) == 1:
            return self.__get_katana_by_no(candidates[0][0])
        else:
            # select
            print('Multiple katanas were found')
            for uid, katana_name in candidates:
                print(f' {uid:>3d}: {katana_name}')
            selected = input('Selected Katana No')
            return self.__get_katana_by_no(selected)

    def __search_katana(self, name: str) -> List[Tuple[str, str]]:
        candidates = []
        for uid, info in self.__data.items():
            katana_name = info.get('display_name', '')
            if name in katana_name:
                candidates += [(uid, katana_name)]
        return candidates
