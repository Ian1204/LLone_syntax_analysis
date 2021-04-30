#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def predict(symDF, tokenSeq, startSym):
    """ 结合预测分析表进行归约
    Args:
        symDF: dataframe 预测分析表
        tokenSeq: list token序列
        startSym: str 起始符号
    """
    symStack = ['#', startSym]
    strStack = tokenSeq + ['#']
    strStack.reverse()

    def stackFormat(st):
        return ''.join(reversed(st))

    """start predicting"""
    while True:
        # over condition
        if symStack == ['#'] and strStack == ['#']:
            print('accept!')
            break

        sym, ch = symStack[-1], strStack[-1]
        if sym == ch:
            print('{0} {1}-{2} passed {0}'.format('-'*50, sym, ch))
            print(' '.join(symStack))
            symStack.pop()
            strStack.pop()
            continue
        else:
            try:
                geneStr = symDF.loc[sym, ch]
                if geneStr == 'err':
                    print('unexcept sym {} and char {}'.format(sym, ch))
                    break
                print('{0} {1}-{2} {0}'.format('-'*50, sym, ch))
                print('{:110}{} -> {}'.format(' '.join(symStack), sym, geneStr))
                symStack.pop()
                if geneStr != '$':
                    symStack += reversed(geneStr.split(' '))
            except Exception as err:
                print('err: {}\nunexcept sym {} and char {}'.format(err, sym, ch))
                break


if __name__ == '__main__':
    df = pd.read_csv('testdata.csv', index_col=0)
    strStack = list('i*i+i#')
    strStack.reverse()
    predict(df, strStack, 'E')
