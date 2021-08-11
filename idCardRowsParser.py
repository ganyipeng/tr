# -*- coding: utf-8 -*- 
# @Time 2021/8/11 11:27

id_card_keys = ('姓名', '性别', '民族', '出生', '住址', '公民身份号码')


def map_value(arr):
    """
    :param arr: [["姓名"], ["邵培远"], ["性别"], ["男"], ["民族汉"]]
    :return: ['姓名', '邵培远', '性别', '男', '民族汉']
    """
    return arr[0].replace(" ", '')


def check_value(arr):
    """
    :param arr: ['姓名', '邵培远', '性别', '男', '民族汉']
    :return: ['姓名', '邵培远', '性别', '男', '民族', '汉']
    """
    result = []
    for key in arr:
        if key[0:2] in id_card_keys and key not in id_card_keys:
            result.append(key[0:2])
            result.append(key[2:])
        else:
            result.append(key)
    return result


def parse(rows):
    str_array = list(map(map_value, rows))
    str_array = check_value(str_array)
    # print(rows)
    # print(str_array)
    # print(id_card_keys)
    id_card_dict = {
        '姓名': '',
        '性别': '',
        '民族': '',
        '出生': '',
        '住址': '',
        '公民身份号码': ''
    }
    i = 0
    while i < len(str_array):
        if str_array[i] in id_card_keys:
            id_key = str_array[i]
            id_card_dict[id_key] = ''
            i += 1
            while i < len(str_array) and str_array[i] not in id_card_keys:
                id_card_dict[id_key] += str_array[i]
                i += 1

    return id_card_dict


