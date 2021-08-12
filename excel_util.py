# -*- coding: utf-8 -*- 
# @Time 2021/8/12 14:06
# pip install openpyxl
from openpyxl import Workbook


def create_xlsx(table_data, xlsx_file_path):
    workbook = Workbook()

    # 默认sheet
    sheet = workbook.active
    sheet.title = "sheet1"
    # sheet = workbook.create_sheet(title="新sheet")
    # sheet.append(columns)
    for data in table_data:
        sheet.append(data)

    workbook.save(xlsx_file_path)
