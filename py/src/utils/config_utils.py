# coding: utf-8

__all__ = ['KatanaInfo', 'read_data', 'read_possessed']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import json
from typing import Any, Dict, NewType, Union

import pandas

KatanaInfo = NewType(
    'KatanaInfo', Dict[str, Union[str, Dict[str, int]]])
FILENAME = './data/katana.json'
POSSESSED = '../../possessed.csv'


def read_data() -> Dict[str, KatanaInfo]:
    with open(FILENAME, encoding='utf8') as data_file:
        return json.load(data_file)


def read_possessed() -> pandas.core.frame.DataFrame:
    df = pandas.read_csv(
        POSSESSED,
        encoding='cp932',
        dtype={'No.': str})
    df.index = df['No.']
    return df
