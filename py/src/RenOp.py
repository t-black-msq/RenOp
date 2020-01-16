# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from optimizer import RenketsuOptimizer
from utils import check_possessed, read_avant


def main():
    # 50
    print('=======================================================')
    print('  RenOp (RenketsuOptimizer)')
    print('      (c) t-black-msq <t.black.msq@gmail.com> 2020-')
    print('=======================================================')
    check_possessed()
    select_mode('本数最小化 + レアリティ', None, 1, 0)
    select_mode('余剰最小化', read_avant(), 0, 1)
    select_mode('本数最小化 + 余剰最小化 + レアリティ', read_avant())
    print('-------------------------------------------------------')
    input('Press Enter to Exit')


def select_mode(
        name: str, data: str = None, weightA: int = 10, weightB: int = 1):
    optimizer = RenketsuOptimizer(data)
    optimizer.add_objective()
    optimizer.make_problem(weightA, weightB)
    optimizer.optimize()
    print('-------------------------------------------------------')
    print(f'  候補: {name} を考慮')
    optimizer.print_(False)
    optimizer.write_possessed()


if __name__ == '__main__':
    main()
