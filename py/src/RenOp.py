# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from optimizer import RenketsuOptimizer
from utils import check_possessed, read_avant

# max選択のとき，
# ほかの候補 (同じだけ上昇する刀を表示する)


def main():
    # 50
    print('============================================================')
    print('  RenOp (RenketsuOptimizer)')
    print('      (c) t-black-msq <t.black.msq@gmail.com> 2020-')
    print('============================================================')
    check_possessed()
    select_mode('本数最小化 + レアリティ', 'A', None, 1, 0)
    select_mode('余剰最小化', 'B', read_avant(), 0, 1)
    select_mode('本数最小化 + 余剰最小化 + レアリティ', 'C', read_avant())
    print('------------------------------------------------------------')
    input('Press Enter to Exit')


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
    print(f'  {name} を考慮した候補')
    optimizer.print_(False)
    optimizer.write_possessed(id_)


if __name__ == '__main__':
    main()
