import pandas as pd
import numpy as np

rules = {'S': [['func']],
         'arg': [[',', 'type', 'IDN', 'arg'], ['$']],
         'args': [['type', 'IDN', 'arg'], ['$']],
         'assign_stmt': [['expression', ';']],
         'block': [['{'], ['stmts'], ['}']],
         'bool_expression': [['lop', 'expression bool_expression'], ['$']],
         'branch_stmt': [['if', '(', 'logical_expression', ')', 'block', 'return']],
         'call_func': [['(', 'es', ')'], ['$']],
         'compare_op': [['>'], ['>='], ['<'], ['<='], ['=='], ['!=']],
         'const': [['num_const'], ['FLOAT'], ['CHAR'], ['STR']],
         'equal_op': [['='], ['+='], ['-='], ['*='], ['/='], ['%=']],
         'es': [['isnull_expr', 'isnull_es']],
         'expression': [['value', 'operation']],
         'factor': [['(', 'value', ')'], ['IDN', 'call_func'], ['const']],
         'func': [['type', 'func_name', '(', 'args', ')', 'func_body']],
         'func_body': [[';'], ['block']],
         'func_name': [['IDN'], ['main']],
         'isnull_es': [[',', 'isnull_expr', 'isnull_es'], ['$']],
         'isnull_expr': [['expression'], ['$']],
         'item': [['factor', "item'"]],
         "item'": [['*', 'factor', "item'"],
                   ['/', 'factor', "item'"],
                   ['%', 'factor', "item'"],
                   ['$']],
         'iteration_stmt': [['while', '(', 'logical_expression', ')', 'block'],
                            ['for',
                             '(',
                             'isnull_expr',
                             'isnull_expr',
                             'isnull_expr',
                             ')',
                             'block']],
         'jump_stmt': [['continue', ';'], ['break', ';'], ['return', 'isnull_expr']],
         'logical_expression': [['!', 'expression bool_expression'],
                                ['expression', 'bool_expression']],
         'lop': [['&&'], ['||']],
         'num_const': [['INT']],
         'operation': [['compare_op', 'value'],
                       ['equal_op', 'value'],
                       ['++'],
                       ['--'],
                       ['$']],
         'result': [['else', 'block'], ['$']],
         'stmts': [['stmt', 'stmts'],
                   ['$']],
         'stmt':  [['type', 'assign_stmt'],
                   ['jump_stmt'],
                   ['iteration_stmt'],
                   ['branch_stmt']],
         'type': [['int'], ['char'], ['float'], ['void'], ['$']],
         'value': [['item', "value'"]],
         "value'": [['+', 'item', "value'"], ['-', 'item', "value'"], ['$']],
         'vars': [[',', 'IDN', 'init', 'vars'], ['$']]}
end_chars = ['while', 'for', 'continue', 'break', 'if', 'else', 'float', 'int', 'char', 'void', 'return', 'main',
             '+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=', '!=', '++', '--', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=',
             '(', ')', '{', '}', ';', ',', '[', ']', '$',
             'IDN', 'INT', 'FLOAT', 'CHAR', 'STR']  # 终结符集
not_end_chars = ['S', 'func', 'type', 'args', 'arg', 'func_body', 'block', 'vars', 'stmts', 'stmt', 'assign_stmt',
                 'jump_stmt', 'iteration_stmt', 'branch_stmt', 'result', 'logical_expression', 'bool_expression', 'lop',
                 'isnull_expr', 'expression', 'operation', 'compare_op', 'equal_op', 'value', "value'", 'item', "item'",
                 'factor', 'call_func', 'es', 'isnull_es', 'const', 'num_const']  # 非终结符集
first_list = {}
follow_list = {}


def get_first_list(grammers):  # 获得FIRST集
    changed = True  # 终止条件，当first集合不变后退出循环
    for i in grammers:
        first_list[i] = []  # 创建First集合
    while changed:  # 上次改变则继续循环
        changed = False
        for cur_char in grammers:
            for rule_right in grammers[cur_char]:  # 对每个产生式右部
                # print('rule_right:', rule_right)
                if rule_right[0] in end_chars:  # 当第一个是终结符时
                    if rule_right[0] not in first_list[cur_char]:
                        first_list[cur_char].append(rule_right[0])
                        changed = True
                else:  # 是非终结符
                    for num in range(len(rule_right)):
                        if rule_right[num] in end_chars:  # 如果循环到终结符，就停止循环
                            if rule_right[num] not in first_list[cur_char]:
                                first_list[cur_char].append(
                                    rule_right[num])
                                changed = True
                            break
                        # 如果是非终结符且这个非终结符的First集合含有空集
                        if rule_right[num] in not_end_chars and '$' in first_list[rule_right[num]]:
                            translist = first_list[rule_right[num]][:]
                            translist.remove('$')
                            if rule_right[num] not in first_list[cur_char]:  # 未加入过这个First集合
                                for new_member in translist:
                                    if new_member not in first_list[cur_char]:
                                        first_list[cur_char].append(
                                            new_member)
                                        changed = True
                        elif '$' not in first_list[rule_right[num]]:
                            translist = first_list[rule_right[num]][:]
                            if rule_right[num] not in first_list[cur_char]:  # 未加入过这个First集合
                                for new_member in translist:
                                    if new_member not in first_list[cur_char]:
                                        first_list[cur_char].append(
                                            new_member)
                            break
    # *debug
    print('First:')
    for i, j in first_list.items():
        print(i, ':', j)


def get_follow_list(grammers):
    changed = True
    for i in grammers:
        follow_list[i] = []
    for i in grammers:  # 初态添加#符号
        follow_list[i].append('#')
        break
    end_char_words = []
    for word in grammers:
        end_char_words.append(word)
    while changed:
        changed = False
        for end_char in grammers:
            for word in grammers[end_char]:
                for num in range(len(word)):
                    if word[num] not in end_char_words:  # 是非终结符，跳到下一个
                        continue
                    else:  # 是终结符
                        if num == len(word)-1:  # 当是最后一个的时候，将Follow(A) 添加到 Follow(B)中
                            # 获取Follow(A)的拷贝
                            help_add = follow_list[end_char][:]
                            for one_add in help_add:
                                if one_add not in follow_list[word[num]]:
                                    follow_list[word[num]].append(one_add)
                                    changed = True
                        else:  # 如果不是最后一个 1. 后面是终结符 2. 后面是非终结符
                            if word[num+1] not in end_char_words:  # 后面是终结符
                                if word[num+1] not in follow_list[word[num]]:
                                    follow_list[word[num]].append(word[num+1])
                                    changed = True
                            else:  # 后面是非终结符
                                # 复制First(B)
                                help_add = first_list[word[num+1]][:]
                                for one_add in help_add:
                                    if one_add not in follow_list[word[num]] and one_add != '$':
                                        follow_list[word[num]].append(one_add)
                                        changed = True
                                    elif one_add == '$' and (num+1) == len(word)-1:
                                        other_help_add = follow_list[end_char][:]
                                        for other_add in other_help_add:
                                            if other_add not in follow_list[word[num]]:
                                                follow_list[word[num]].append(
                                                    other_add)
                                                changed = True
    print('Follow:')
    for i, j in follow_list.items():
        print(i, ':', j)


def get_analysis_table():
    df = pd.DataFrame(data='err', index=not_end_chars, columns=end_chars)
    for char in not_end_chars:
        for one_char in first_list[char]:
            for str in rules[char]:
                if str == '$':  # 当first集合含有空的时候
                    for follow_char in follow_list[char]:
                        df.loc[char, follow_char] = '$'
                elif str[0] == one_char:
                    fill_in = ''
                    for i in str:
                        fill_in += i
                        fill_in += ' '
                    df.loc[char, one_char] = fill_in
                elif str[0] in not_end_chars:
                    for num in range(len(str)):
                        if str[num] in not_end_chars:
                            if one_char in first_list[str[num]]:
                                fill_in = ''
                                for i in str:
                                    fill_in += i
                                    fill_in += ' '
                                df.loc[char, one_char] = fill_in
                                break
                            elif '$' in first_list[str[num]]:
                                continue
                        elif str[num] == one_char:
                            fill_in = ''
                            for i in str:
                                fill_in += i
                                fill_in += ' '
                            df.loc[char, one_char] = fill_in
                            break
    df.to_csv('table.csv')


if __name__ == '__main__':
    get_first_list(rules)
    get_follow_list(rules)
    get_analysis_table()
