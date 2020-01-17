# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

import os

from optimizer import RenketsuOptimizer
from utils import check_possessed, read_avant, reset_mode_avant

# max選択のとき，
# ほかの候補 (同じだけ上昇する刀を表示する)


def main():
    print('============================================================')
    print('  RenOp (RenketsuOptimizer)')
    print('      (c) t-black-msq <t.black.msq@gmail.com> 2020-')
    print('============================================================')
    check_possessed()
    key = ()
    optimizerA = select_mode('本数最小化 + レアリティ', 'A', None, 1, 0)
    if optimizerA.output:
        key += ('A',)
    optimizerB = select_mode('余剰最小化', 'B', read_avant(), 0, 1)
    if optimizerB.output:
        key += ('B',)
    optimizerC = select_mode('本数最小化 + 余剰最小化 + レアリティ', 'C', read_avant())
    if optimizerC.output:
        key += ('C',)
    # D: 余剰を生まない範囲で最大 (select_mode2)
    print('------------------------------------------------------------')
    if optimizerA.is_infeasible or optimizerB.is_infeasible or optimizerC.is_infeasible:
        optimizerC.use_all()
        print('------------------------------------------------------------')

    reset_mode_avant()

    if not optimizerC.is_max:
        decide(key)


def select_mode(
        name: str,
        id_: str,
        data: str = None,
        weightA: int = 10,
        weightB: int = 1):
    optimizer = RenketsuOptimizer(data)
    optimizer.add_objective()
    optimizer.make_problem(weightA, weightB)
    optimizer.optimize()
    print('------------------------------------------------------------')
    print(f' {id_}: {name} を考慮した候補')
    optimizer.print_(False)
    if optimizer.is_infeasible:
        optimizer2 = RenketsuOptimizer(read_avant())
        optimizer2.add_objective()
        optimizer2.make_problem2(weightA, weightB)
        optimizer2.optimize()
        optimizer2.print_(False)
    else:
        optimizer.write_possessed(id_)

    return optimizer


def decide(key: tuple = ('A', 'B', 'C')):
    if key:
        print(f'提示した候補で錬結する場合、候補ID ({" or ".join(key)})を入力してください')
        print('possessed.csvの刀剣所持数が錬結後の値に書き換えられます')
        print('※ それ以外の文字を入力すると終了します')
        id_ = input('?: ')
        if id_ in key:
            os.rename('data/possessed.csv', 'data/possessed.csv.old')
            os.rename(f'data/possessed_new_{id_}.csv', 'data/possessed.csv')
            for k in key:
                if k != id_:
                    os.remove(f'data/possessed_new_{k}.csv')
        else:
            for k in key:
                os.remove(f'data/possessed_new_{k}.csv')
            os._exit(1)


if __name__ == '__main__':
    main()
