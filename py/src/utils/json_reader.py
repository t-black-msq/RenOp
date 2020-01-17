# coding: utf-8

__all__ = ['reflect_to_possessed']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import json
from typing import List

import pandas

from .config_utils import read_possessed, write_possessed

FILENAME = 'data/data.json'
POSSESSED = 'data/possessed.csv'


def read():
    with open(FILENAME, encoding='utf8') as file:
        return json.load(file)


def get_sword_list() -> List[str]:
    swords = read().get('sword')
    uids = []
    for serial_id, sword in swords.items():
        # 乱舞レベルが上がっている刀剣はスキップ
        if sword.get('ranbu_exp') != '0':
            continue
        # 経験値が上がっている刀剣はスキップ
        if sword.get('exp') != '0':
            continue
        # 保護されている刀剣はスキップ
        if sword.get('protect') != '0':
            continue
        # お守りを装備している刀剣はスキップ
        if sword.get('item_id') is not None:
            continue
        # 馬を装備している刀剣はスキップ
        if sword.get('horse_serial_id') is not None:
            continue
        # 刀装を装備している刀剣はスキップ
        equip = False
        for i in range(1, 4):
            if sword.get(f'equip_serial_id{i}') is not None:
                equip = True
                break
        if equip:
            continue

        uids += [f'{int(sword.get("sword_id")):03d}']

    return uids


def reflect_to_possessed():
    possessed = read_possessed()
    swords = get_sword_list()
    for idx in possessed.index:
        possessed.at[idx, '所持数'] = swords.count(idx)

    write_possessed(possessed)


if __name__ == '__main__':
    reflect_to_possessed()
