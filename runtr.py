# coding: utf-8
import tr
import sys, cv2, time, os
from PIL import Image, ImageDraw, ImageFont
import numpy
import csv
import getVerticalBorder

_BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASEDIR)

def get_table(ocr_results, row_x):
    '''
    对ocr的结果进行整理，根据结果中的位置信息整理出表格
    :param ocr_results: ocr的带位置结果
    :param row_x: 表格中每条竖线x坐标
    :return: 表格形式的数据
    '''
    data_all = []  # 存储所有的数据
    data_count = 0  # 统计数据的数目
    for i, rect in enumerate(ocr_results):
        cx, cy, w, h, a = tuple(rect[0])
        tmp_data = []  # 数据的形式为[x,y,value]，其中x和y为中心的坐标
        tmp_data.append(cx)
        tmp_data.append(cy)
        tmp_data.append(rect[1])
        data_all.append(tmp_data)
        data_count = data_count + 1

    data_lines = []  # 存储分行之后的数据
    tmp_line = []   # 临时变量，收集每行的数据
    tmp_line.append(data_all[0])
    for i in range(1, data_count):
        if abs(data_all[i][1] - data_all[i - 1][1]) < 10: # y坐标相差不超过10则被认为是同一行
            tmp_line.append(data_all[i])
        else:
            if tmp_line:
                data_lines.append(tmp_line)
            tmp_line = []
            tmp_line.append(data_all[i])
    data_lines.append(tmp_line)

    res = []  # 最终的结果，其中只存放了value
    for i in range(len(data_lines)):  # i遍历剩下的行
        # print(data_lines[i])
        tmp_line = []  # 用来帮助收集value的临时变量，每次收集一行
        for k in range(len(row_x)-1):
            tmp_line.append("")
        for data in data_lines[i]:
            loc_x = float(data[0])
            value = data[2]
            for x_index in range(1, len(row_x)): # 根据竖线坐标对每行数据进行列的划分
                if loc_x < row_x[x_index]:
                    tmp_line[x_index - 1] += value
                    break
        res.append(tmp_line)
    return res


def run_tr(img_path):
    '''
    运行对图片进行处理，然后运行tr
    :param img_path: 图片路径
    :return: 格式化的表格数据
    '''
    img_pil = Image.open(img_path)
    init_width = img_pil.width
    try:
        if hasattr(img_pil, '_getexif'):
            orientation = 274
            exif = dict(img_pil._getexif().items())
            if exif[orientation] == 3:
                img_pil = img_pil.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img_pil = img_pil.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img_pil = img_pil.rotate(90, expand=True)
    except:
        pass

    MAX_SIZE = 1600 # 图片的大小最好不超过 1600
    scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

    new_width = int(img_pil.width / scale + 0.5)
    new_height = int(img_pil.height / scale + 0.5)
    img_pil = img_pil.resize((new_width, new_height), Image.ANTIALIAS)

    img_cv = cv2.cvtColor(numpy.asarray(img_pil), cv2.COLOR_RGB2BGR)
    row_x = getVerticalBorder.get_row_x(img_cv) # 获取表格竖线的坐标
    print(row_x)

    print('len :::', len(img_pil.split()))

    img_pil_split = img_pil.split()
    img_pil_split_len = len(img_pil_split)

    if img_pil_split_len == 3:
        r, g, b = img_pil_split
        img_pil = r # 取印章不明显的通道
    elif img_pil_split_len == 4:
        r,g,b,a = img_pil_split
        img_pil = r

    threshold = 150 # 对图片进行二值化的阈值，进一步抹除印章

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    
    if init_width > 500:
        print('init_width', init_width)
        # img_pil = img_pil.point(table, "1") # 对图片进行二值化

    ocr_results = tr.run(img_pil, flag=tr.FLAG_RECT) #运行tr，获得带位置的ocr结果
    res = get_table(ocr_results, row_x)
    return res



