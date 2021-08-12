import fitz
from runtr import run_tr
import csv
import os
from excel_util import create_xlsx

def write_csv(res_data, res_file):
    with open(res_file, "w") as res_f:
        writer = csv.writer((res_f))
        for line in res_data:
            writer.writerow(line)


def table_get(fileName, image_type):
    res_data = run_tr(fileName+'.'+image_type)
    print('res_data:::::::::::::')
    print(res_data)
    # write_csv(res_data, img_path+".csv")
    create_xlsx(res_data, fileName+'.xlsx')
    return res_data


