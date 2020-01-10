# coding: utf-8

__all__ = []
__author__ = 't-black-msq <t.black.msq@gmail.com>'

from optimizer import RenketsuOptimizer


def main():
    optimizer = RenketsuOptimizer()
    optimizer.add_objective()
    optimizer.optimize()