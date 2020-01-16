# coding: utf-8

__all__ = [
    'KatanaInfo',
    'check_possessed',
    'read_avant',
    'read_data',
    'read_possessed',
    'write_avant']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import json
import os
from typing import Any, Dict, NewType, Union

import pandas

KatanaInfo = NewType(
    'KatanaInfo', Dict[str, Union[str, Dict[str, int]]])
FILENAME = './data/katana.json'
POSSESSED = './data/possessed.csv'
AVANT = './data/avant.dat'


def read_data() -> Dict[str, KatanaInfo]:
    """katana.jsonを読み込む

    Returns
    -------
    dict
        刀剣データ
    """
    with open(FILENAME, encoding='utf8') as data_file:
        return json.load(data_file)


def read_possessed() -> pandas.core.frame.DataFrame:
    """possessed.csvを読み込む

    Returns
    -------
    pandas.core.frame.DataFrame
        錬結に使用する所有刀剣データ
    """
    df = pandas.read_csv(
        POSSESSED,
        encoding='cp932',
        dtype={'No.': str})
    df.index = df['No.'].apply(lambda x: f'{int(x):03d}')
    return df


def check_possessed():
    """possessed.csvの中身をチェックする．所有刀剣がない場合はアプリを中断する．
    """
    possessed = read_possessed()
    if possessed.sum().at['所持数'] == 0:
        os._exit(1)


def read_avant() -> str:
    with open(AVANT, encoding='utf8') as avant:
        return avant.read().strip()


def write_avant(data: str):
    with open(AVANT, 'w', encoding='utf8') as avant:
        avant.write(data)
