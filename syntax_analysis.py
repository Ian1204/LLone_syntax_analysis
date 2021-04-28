
rules = {'S': [['func']],
         'func': [['type', 'IDN', '(', 'args', ')', 'func_body']],
         'type': [['int'], ['char'], ['float'], ['void'], ['$']],
         'args': [['type', 'IDN', 'arg'], ['$']],
         'arg': [[',', 'type', 'IDN', 'arg'], ['$']],
         'func_body': [[';'], ['block']],
         'block': [['{'], ['stmts'], ['}']],
         'vars': [[',', 'IDN', 'init', 'vars'], ['$']],
         'stmts': [['stmt', 'stmts'], ['$'], ['type', 'assign_stmt'], ['jump_stmt'], ['iteration_stmt'], ['branch_stmt']],
         'assign_stmt': [['expression', ';']],
         'jump_stmt': [['continue', ';'], ['break', ';'], ['return', 'isnull_expr']],
         'iteration_stmt': [['while', '(', 'logical_expression', ')', 'block'], ['for', '(', 'isnull_expr', 'isnull_expr', 'isnull_expr', ')', 'block']],
         'branch_stmt': [['if', '(', 'logical_expression', ')', 'block', 'return']],
         'return': [['else' 'block'], ['$']],
         'logical_expression': [['!', 'expression bool_expression'], ['expression', 'bool_expression']],
         'bool_expression': [['lop', 'expression bool_expression'], ['$']],
         'lop': [['&&'], ['||']],
         'isnull_expr': [['expression'], ['$']],
         'expression': [['value', 'operation']],
         'operation': [['compare_op', 'value'], ['equal_op', 'value'], ['++'], ['--'], ['$']],
         'compare_op': [['>'], ['>='], ['<'], ['<='], ['=='], ['!=']],
         'equal_op': [['='], ['+='], ['-='], ['*='], ['/='], ['%=']],
         'value': [['item', "value'"]],
         "value'": [['+', 'item', "value'"], ['-', 'item', "value'"], ['$']],
         'item': [['factor', "item'"]],
         "item'": [['*', 'factor', "item'"], ['/', 'factor', "item'"], [' % ', 'factor', "item'"], ['$']],
         'factor': [['(', 'value', ')'], ['IDN', 'call_func'], ['const']],
         'call_func': [['(', 'es', ')'], ['$']],
         'es': [['isnull_expr', 'isnull_es']],
         'isnull_es': [[',', 'isnull_expr', 'isnull_es'], ['$']],
         'const': [['num_const'], ['FLOAT'], ['CHAR'], ['STR']],
         'num_const': [['INT']]
         }
end_chars = ['while', 'for', 'continue', 'break', 'if', 'else', 'float', 'int', 'char', 'void', 'return',
             '+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=', '!=', '++', '--', '&&', '||', '+=', '-=', '*=', '/=', '%=',
             '(', ')', '{', '}', ';', ',', '[', ']', '$',
             'IDN', 'INT', 'FLOAT', 'CHAR', 'STR']  # 终结符集
not_end_chars = ['S', 'func', 'type', 'args', 'arg', 'func_body', 'block', 'vars', 'stmts', 'stmt', 'assign_stmt',
                 'jump_stmt', 'iteration_stmt', 'branch_stmt', 'result', 'logical_expression', 'bool_expression', 'lop',
                 'isnull_expr', 'expression', 'operation', 'compare_op', 'equal_op', 'value', "value'", 'item', "item'",
                 'factor', 'call_func', 'es', 'isnull_es', 'const', 'num_const']  # 非终结符集


def get_first_list(grammers):  # 获得FIRST集
    changed = True  # 终止条件，当first集合不变后退出循环
    new_First = {}
    for i in grammers:
        new_First[i] = []  # 创建First集合
    while changed:  # 上次改变则继续循环
        changed = False
        for end_char in grammers:
            # *debug
            # print('end_char:', end_char)
            for rule_right in grammers[end_char]:  # 对每个产生式右部
                # *debug
                # print('rule_right:', rule_right)
                if rule_right[0] not in end_chars:  # 当不是终结符时
                    # *debug
                    # print('rule_right[0]:', rule_right[0])
                    if rule_right[0] not in new_First[end_char]:
                        new_First[end_char].append(rule_right[0])
                        changed = True
                else:
                    for num in range(len(rule_right)):
                        if rule_right[num] in end_chars:  # 如果循环到终结符，就停止循环
                            if rule_right[num] not in new_First[end_char]:
                                new_First[end_char].append(rule_right[num])
                                changed = True
                            break
                        # 如果是非终结符且这个非终结符的First集合含有空集
                        if rule_right[num] in not_end_chars and '$' in new_First[rule_right[num]]:
                            translist = new_First[rule_right[num]][:]
                            translist.remove('$')
                            if rule_right[num] not in new_First[end_char]:  # 未加入过这个First集合
                                for new_member in translist:
                                    if new_member not in new_First[end_char]:
                                        new_First[end_char].append(new_member)
                                        changed = True
                        elif '$' not in new_First[rule_right[num]]:
                            translist = new_First[rule_right[num]][:]
                            if rule_right[num] not in new_First[end_char]:  # 未加入过这个First集合
                                new_First[end_char] = new_First[end_char] + translist
                                changed = True
                            break
    print('First:')
    for i, j in new_First.items():
        print(i, ':', j)
    return new_First


if __name__ == '__main__':
    get_first_list(rules)
