# coding: utf-8

__all__ = ['RenketsuModel']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import mipcl_py.mipshell.mipshell as mp


class RenketsuModel(mp.Problem):
    """"""

    def __init__(self, model_name: str):
        super().__init__(model_name)