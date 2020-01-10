# coding: utf-8

__all__ = ['KatanaInfo', 'read_data']
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import json
from typing import Any, Dict, NewType, Union

KatanaInfo = NewType('KatanaInfo', Dict[str, Dict[str, Union[str, Dict[str, int]]]])
FILENAME = './data/katana.json'

def read_data() -> KatanaInfo:
    with open(FILENAME, encoding='utf8') as data_file:
        return json.load(data_file)