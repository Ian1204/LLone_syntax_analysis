import re


symtable = ['while', 'for', 'continue', 'break', 'if', 'else', 'float', 'int', 'char', 'void', 'return', 'main',
            '+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=', '!=', '++', '--', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=',
            '(', ')', '{', '}', ';', ',', '[', ']',
            'IDN', 'INT', 'FLOAT', 'CHAR', 'STR']


def getData(url):
    with open(url, 'r') as f:
        data = f.read()
    return data


def getIdx(s):
    return symtable.index(s)


def isStr(s):
    return re.match('[a-zA-Z0-9_]', s)


def analyse(data):
    """ 对代码进行词法分析 返回token序列
    Args: 
        data: str 代码
    Rets:
        strStack: list token序列
    """
    i = 0  # 字符指针
    line = 1  # 行指针
    ret = []  # 返回列表
    """ 当小于长度时loop """
    while i < len(data):
        # 忽略空格和制表符
        if data[i] == ' ' or data[i] == '\t':
            i += 1
            continue
        # 进入下一行
        if data[i] == '\n':
            line += 1
            i += 1
            continue

        if data[i].isdigit():
            start = i
            isFloat = False
            while data[i].isdigit() or data[i] == '.':
                if data[i] == '.':
                    if isFloat:
                        raise Exception(
                            'more than 1 dot for a float type at line: %d', line)
                    isFloat = True
                i += 1
            # if data[i] != ' ' or '\n':
            #     raise Exception('invalid number in line: %d', line)
            num = data[start:i]
            if isFloat:
                ret.append((getIdx('FLOAT'), num))
            else:
                ret.append((getIdx('INT'), num))
            continue
        # data[i] is char and data[i] can't belong to 0-9
        # this if statement is to get symbol
        elif isStr(data[i]):
            start = i
            while isStr(data[i]):
                i += 1
            sym = data[start:i]
            if sym in symtable:
                ret.append((getIdx(sym), None))
            else:
                ret.append((getIdx('IDN'), sym))
            continue
        # this if statement is to get char or str
        elif data[i] == '\'' or data[i] == '\"':
            if data[i] == '\"':
                i += 1
                start = i
                while data[i] != '\"':
                    # 对行数要处理
                    if data[i] == '\n':
                        line += 1
                    i += 1
                s = data[start:i]
                ret.append((getIdx('STR'), s))
                i += 1
                continue
            elif data[i] == '\'' and isStr(data[i+1]) and data[i+2] == '\'':
                ret.append((getIdx('CHAR'), data[i+1]))
                i += 3
                continue
            else:
                raise Exception("str or char analyse failed in line: %d", line)
        # this if statement is to get SE (界符)
        elif data[i] in ['(', ')', '{', '}', ';', ',', '[', ']']:
            ret.append((getIdx(data[i]), None))
            i += 1
            continue
        # this if statement is to get OP
        else:
            op1, op2 = data[i], data[i:i+2]
            posSym = ['+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=',
                      '!=', '++', '--', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=']
            if op2 in posSym:
                ret.append((getIdx(op2), None))
                i += 2
            elif op1 in posSym:
                ret.append((getIdx(op1), None))
                i += 1
            else:
                raise Exception('invalid op in line: %d' % line)
            continue
    strStack = []
    for i in ret:
        strStack.append(symtable[i[0]])
    # 打印token序列
    print('token序列:', strStack)
    # 打印符号表
    print('\n符号表:')
    OP = ['+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=', '!=', '++', '--', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=']
    SE = ['(', ')', '{', '}', ';', ',', '[', ']']
    for i in ret:
        ch = i[1] if i[1] else '_'
        sym = symtable[i[0]]
        c = i[1] if i[1] else symtable[i[0]]
        if sym in OP:
            sym = 'OP'
        elif sym in SE:
            sym = 'SE'
        elif sym == 'INT':
            sym = 'CONST'
        else:
            sym = sym.upper()
        print('{} <{}, {}>'.format(c, sym, ch))
    


    return strStack


def main():
    data = getData('test5.c')
    ret = analyse(data)
    # print(ret)
    print('词法分析结果如下：')
    for i in ret:
        print("<{},{}>".format(symtable[i[0]], i[1]))


if __name__ == '__main__':
    main()
