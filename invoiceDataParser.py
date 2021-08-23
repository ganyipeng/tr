# -*- coding: utf-8 -*- 
# @Time 2021/8/23 10:31


def get_rows(result_values: 'str_list'):
    return [result_values[0:4], result_values[4:12], result_values[12:14], result_values[14:18], result_values[18], result_values[19]]


def parse_row0(arg_row: 'list'):
    # ["购  \n买  \n方  \n",
    #  "名  称:  山东中创软件工程股份有限公司  \n纳税人识别号:  913700007059570053  \n地址、电话:  \n电子支付标识:  \n",
    #  "密  \n码  \n区  \n",
    #  "0  1  9  3  8  0  6  e  3  d      f  a  3  3  e  2…4  c  c  8  7      7  d b  5  7  b  c  b  a  4  \n"]
    row0_dict = {}
    cell_1 = arg_row[1]
    texts = cell_1.split("\n")
    texts = [text.strip() for text in texts]
    row0_dict['name'] = texts[0].split(':')[1].strip()
    row0_dict['registerNum'] = texts[1].split(':')[1].strip()
    row0_dict['addressAndPhone'] = texts[2].split(':')[1].strip()
    return {'purchaser': row0_dict}


def parse_row1(arg_row: 'list'):
    # ["货物或应税劳务、服务名称  \n*其他软件服务*微信平台服务  \n合  计  \n",
    #           "规格型号  \n无  \n",
    #           "单位  \n项  \n",
    #           "数量  \n1  \n",
    #           "单价  \n283.02  \n",
    #           "金  额  \n283.02  \n¥283.02  \n",
    #           "税率  \n6%  \n",
    #           "税  额  \n16.98  \n¥16.98  \n",]
    row1_dict = {}
    cells = [cell.split("\n") for cell in arg_row]
    items_count = len(cells[0]) - 3
    items = []
    for dict_index in range(items_count):
        item_dict = {'row': dict_index}
        cell_index = dict_index + 1
        cell = cells[0]
        item_dict['name'] = cell[cell_index].strip()
        cell = cells[1]
        item_dict['type'] = cell[cell_index].strip()
        cell = cells[2]
        item_dict['unit'] = cell[cell_index].strip()
        cell = cells[3]
        item_dict['count'] = cell[cell_index].strip()
        cell = cells[4]
        item_dict['price'] = cell[cell_index].strip()
        cell = cells[5]
        item_dict['amount'] = cell[cell_index].strip()
        cell = cells[6]
        item_dict['rate'] = cell[cell_index].strip()
        cell = cells[7]
        item_dict['rateAmount'] = cell[cell_index].strip()
        items.append(item_dict)

    summary = {
        'amount': cells[5][items_count+1].strip(),
        'rateAmount': cells[7][items_count+1].strip()
    }

    return {'items': items, 'summary': summary}


def parse_row2(arg_row: 'list'):
    # "价税合计(大写)  \n",
    #           "凶  叁佰元整  (小写)¥300.00  \n",
    row2_dict = {}
    txt = arg_row[1]
    tt = txt.split(" ")
    cc = [t for t in tt if t != '' and t != '\n']
    if len(cc) == 3:
        row2_dict['upperCase'] = cc[1]
        row2_dict['lowerCase'] = cc[2].split('¥')[1]
    return {'priceTaxSummary': row2_dict}


def parse_row3(arg_row: 'list'):
    # ["销  \n售  \n方  \n",
    #  "名  称:  山东中创软件工程股份有限公司  \n纳税人识别号:  913700007059570053  \n地址、电话:  \n电子支付标识:  \n",
    #  "备  \n注  \n",
    #  "微信认证费已付,请勿转账  \n算机系          \n      91440300708461136T    \n  屮画厶田    \n"]
    seller = {}
    cell_1 = arg_row[1]
    texts = cell_1.split("\n")
    texts = [text.strip() for text in texts]
    seller['name'] = texts[0].split(':')[1].strip()
    seller['registerNum'] = texts[1].split(':')[1].strip()
    seller['addressAndPhone'] = texts[2].split(':')[1].strip()
    seller['bank'] = texts[3].split(':')[1].strip()

    return {'seller': seller}


def parse_peoples(peoples_str: 'list'):
    # "深圳电子普通发票  \n统  友票    发票代码:144032109110  \n  燃  发票号码:07209023  \n架圳市税务朐  \n开票日期:2021年03月24日  \n校验码:bcba4  \n"
    peoples_list = peoples_str.split("\n")
    peoples_str = peoples_list[1]
    peoples_split_blank = peoples_str.split(" ")
    peoples_split_blank_and_remove_blank = [people for people in peoples_split_blank if people != '']
    people_split_colon = [people.split(':') for people in peoples_split_blank_and_remove_blank]
    peoples = {
        'payee': people_split_colon[0][1].strip(),
        'checker': people_split_colon[1][1].strip(),
        'noteDrawer': people_split_colon[2][1].strip()
    }

    return {'seller': peoples}


def parse_invoice_info(invoice_info_str: 'list'):
    # "深圳电子普通发票  \n统  友票    发票代码:144032109110  \n  燃  发票号码:07209023  \n架圳市税务朐  \n开票日期:2021年03月24日  \n校验码:bcba4  \n"
    invoice_info_str = "深圳电子普通发票  \n统  友票    发票代码:144032109110  \n  燃  发票号码:07209023  \n架圳市税务朐  \n开票日期:2021年03月24日  \n校验码:bcba4  \n"
    invoice_info_list = invoice_info_str.split("\n")
    infos = [info.strip() for info in invoice_info_list if info != '']
    invoice_info_dict = {
        "type": infos[0],
        "code": infos[1].split(":")[1],
        "num": infos[2].split(":")[1],
        "date": infos[4].split(":")[1],
        "checkCode": infos[5].split(":")[1]
    }

    return {'invoiceInfo': invoice_info_dict}


def parse(result: 'str_list'):
    rows = get_rows(result)
    dict_0 = parse_row0(rows[0])
    dict_1 = parse_row1(rows[1])
    dict_2 = parse_row2(rows[2])
    dict_3 = parse_row3(rows[3])
    peoples = parse_peoples(rows[4])
    invoice_info = parse_invoice_info(rows[5])
    invoice_dict = {**dict_0, **dict_1, **dict_2, **dict_3, **peoples, **invoice_info}
    return invoice_dict


def _test():

    result = [

            "购  \n买  \n方  \n",
              "名  称:  山东中创软件工程股份有限公司  \n纳税人识别号:  913700007059570053  \n地址、电话:  \n电子支付标识:  \n",
              "密  \n码  \n区  \n",
              "0  1  9  3  8  0  6  e  3  d      f  a  3  3  e  2…4  c  c  8  7      7  d b  5  7  b  c  b  a  4  \n",

              "货物或应税劳务、服务名称  \n*其他软件服务*微信平台服务  \n合  计  \n",
              "规格型号  \n无  \n",
              "单位  \n项  \n",
              "数量  \n1  \n",
              "单价  \n283.02  \n",
              "金  额  \n283.02  \n¥283.02  \n",
              "税率  \n6%  \n",
              "税  额  \n16.98  \n¥16.98  \n",

              "价税合计(大写)  \n",
              "凶  叁佰元整  (小写)¥300.00  \n",

              "销  \n售  \n方  \n",
              "名  称:  深圳市腾讯计算机系统有限公司  \n纳税人识别号:  91440300708461136T  \n地址、电话:  深圳市南山区粤海街道麻岭社区科技中一路腾讯大厦35层0755-86013388  \n开户行及账号:  招商银行深圳威盛大厦支行817282299610001  \n",
              "备  \n注  \n",
              "微信认证费已付,请勿转账  \n算机系          \n      91440300708461136T    \n  屮画厶田    \n",

              "  ~F  \n收款人:微信平台  复核:微信平台  开票人:微信平台  销售方:(章)  (4)      \n03 0 5 5 4 16  6  \n发票查验请登录国家税务总局深圳市税务局网站:  shenzhen.chinatax.gov.cn  (首页>办税服务>涉税查询>发票真伪查验)  \n",

            "深圳电子普通发票  \n统  友票    发票代码:144032109110  \n  燃  发票号码:07209023  \n架圳市税务朐  \n开票日期:2021年03月24日  \n校验码:bcba4  \n"
    ]


    print(parse(result))


if __name__ == '__main__':
    _test()


