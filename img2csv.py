import fitz
from runtr import run_tr
import csv
import os


def write_csv(res_data, res_file):
    with open(res_file, "w") as res_f:
        writer = csv.writer((res_f))
        for line in res_data:
            writer.writerow(line)


def table_get(img_path):
    res_data = run_tr(img_path)
    print('res_data:::::::::::::')
    print(res_data)
    write_csv(res_data, img_path+".csv")
    return res_data


