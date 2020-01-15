# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from optimizer import RenketsuOptimizer


def main():
    print('---------------------------------------------')
    print('  RenOp (RenketsuOptimizer)')
    print('(c) t-black-msq <t.black.msq@gmail.com> 2020-')
    print('---------------------------------------------')
    # check possessed
    optimizer = RenketsuOptimizer()
    optimizer.add_objective()
    optimizer.make_problem()
    optimizer.optimize()
    optimizer.print_()


if __name__ == '__main__':
    main()
