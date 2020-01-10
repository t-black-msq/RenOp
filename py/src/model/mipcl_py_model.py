# coding: utf-8

__all__ = ['RenketsuModel']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import mipcl_py.mipshell.mipshell as mp


class RenketsuModel:
    """"""

    def __init__(self, model_name: str):
        self.__model = mp.Problem(model_name)