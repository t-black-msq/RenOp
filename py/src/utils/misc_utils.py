# coding: utf-8

__all__ = ['is_integer']
__author__ = 't-black-msq <t.black.msq@gmail.com>'


def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False