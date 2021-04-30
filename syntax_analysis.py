import pandas as pd
import numpy as np
from analyzer import analyse, getData
from predicator import predict
from pprint import pprint

# rules = {}  # 文法规则格式化
end_chars = ['while', 'for', 'continue', 'break', 'if', 'else', 'float', 'int', 'char', 'void', 'return', 'main',
             '+', '-', '*', '/', '%', '=', '>', '<', '==', '<=', '>=', '!=', '++', '--', '&&', '||', '!', '+=', '-=', '*=', '/=', '%=',
             '(', ')', '{', '}', ';', ',', '[', ']',
             'IDN', 'INT', 'FLOAT', 'CHAR', 'STR', '$']  # 终结符集
not_end_chars = []  # 非终结符集
# first_list = {}  # first集
# follow_list = {}  # follow集


def get_grammers(url):  # 文法格式化
    rules = {}
    with open(url, 'r') as f:
        lines = f.readlines()
        for line in lines:
            linelist = line.replace('\n', '').split(' ')
            l0 = linelist[0]
            if l0 not in rules:
                not_end_chars.append(l0)
                rules[l0] = []
            del linelist[1], linelist[0]
            rules[l0].append(linelist)
    return rules


def get_first_list(grammers):  # 获得FIRST集
    changed = True  # 终止条件，当first集合不变后退出循环
    first_list = {}
    for i in grammers:
        first_list[i] = []  # 创建First集合
    try:
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
                            # 该非终结符first集没有空集
                            elif '$' not in first_list[rule_right[num]]:
                                translist = first_list[rule_right[num]][:]
                                if rule_right[num] not in first_list[cur_char]:  # 未加入过这个First集合
                                    for new_member in translist:
                                        if new_member not in first_list[cur_char]:
                                            first_list[cur_char].append(
                                                new_member)
                                            changed = True
                                break
    except:
        print('Something wrong when getting first list')
    return first_list


def get_follow_list(grammers, first_list):
    changed = True
    follow_list = {}
    for i in grammers:
        follow_list[i] = []
    for i in grammers:  # 初态添加#符号
        follow_list[i].append('#')
        break
    try:
        while changed:
            changed = False
            for end_char in grammers:
                for rule_right in grammers[end_char]:  # 每个产生式的右部
                    for num in range(len(rule_right)):
                        if rule_right[num] not in not_end_chars:  # 是终结符，跳到下一个
                            continue
                        else:  # 是非终结符
                            # 当是最后一个的时候，将Follow(A) 添加到 Follow(B)中
                            if num == len(rule_right)-1:
                                # 获取Follow(A)的拷贝
                                help_add = follow_list[end_char][:]
                                for one_add in help_add:
                                    if one_add not in follow_list[rule_right[num]]:
                                        follow_list[rule_right[num]].append(
                                            one_add)
                                        changed = True
                            else:  # 如果不是最后一个
                                if rule_right[num+1] not in not_end_chars:  # 后面是终结符
                                    if rule_right[num+1] not in follow_list[rule_right[num]]:
                                        follow_list[rule_right[num]].append(
                                            rule_right[num+1])
                                        changed = True
                                else:  # 后面是非终结符
                                    # 复制First(B)
                                    help_add = first_list[rule_right[num+1]][:]
                                    for one_add in help_add:
                                        if one_add not in follow_list[rule_right[num]] and one_add != '$':
                                            follow_list[rule_right[num]].append(
                                                one_add)
                                            changed = True
                                        elif one_add == '$' and (num+1) == len(rule_right)-1:
                                            other_help_add = follow_list[end_char][:]
                                            for other_add in other_help_add:
                                                if other_add not in follow_list[rule_right[num]]:
                                                    follow_list[rule_right[num]].append(
                                                        other_add)
                                                    changed = True
    except:
        print('Something wrong when getting follow list!')
    return follow_list


# 将预测分析表存入dataframe，方便转换成csv或xlsx格式
def get_analysis_table(rules, first_list, follow_list):
    df = pd.DataFrame(data='err', index=not_end_chars, columns=end_chars)
    for char in not_end_chars:
        for one_char in first_list[char]:  # 对每个first集里面的每个符号
            for str in rules[char]:  # 对每个产生式
                if str == ['$']:  # 当该first集合含有空的时候
                    for follow_char in follow_list[char]:
                        df.loc[char, follow_char] = '$'
                elif str[0] == one_char:  # 产生式右部第一个匹配
                    df.loc[char, one_char] = ' '.join(str)  # 存入用空格隔开的字符串
                elif str[0] in not_end_chars:  # 是非终结符
                    for num in range(len(str)):
                        if str[num] in not_end_chars:
                            if one_char in first_list[str[num]]:
                                df.loc[char, one_char] = ' '.join(str)
                                break
                            elif '$' in first_list[str[num]]:  # 当对应first集合有空集，则继续循环
                                continue
                        elif str[num] == one_char:  # 第num个字符匹配
                            df.loc[char, one_char] = ' '.join(str)
                            break
    # df.to_csv('table.csv')
    return df


def main():
    rules = get_grammers('grammer.txt')
    data = getData('test4.c')
    # 进行词法分析
    try:
        tokenSeq = analyse(data)
    except Exception as err:
        print('err:', err)
        return

    # pprint(rules)
    first_list = get_first_list(rules)
    follow_list = get_follow_list(rules, first_list)
    df_input = get_analysis_table(rules, first_list, follow_list)
    df_input.to_excel('grammertable.xlsx')

    # print('\nFirst:')
    # for i, j in first_list.items():
    #     print(i, ':', j)
    # print('\nFollow:')
    # for i, j in follow_list.items():
    #     print(i, ':', j)

    print('\n规约过程：')
    predict(df_input, tokenSeq, 'S')


if __name__ == '__main__':
    main()
