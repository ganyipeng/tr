import tr
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy
import xlwt
import sys
import split_pic
import remove_seal

def get_value(ocr_results):
    '''
    @param ocr_results: 一个单元格的ocr结果
    @return: 该单元格中的文本内容
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
    tmp_line = []  # 临时变量，收集每行的数据
    tmp_line.append(data_all[0])
    for i in range(1, data_count):
        if abs(data_all[i][1] - data_all[i - 1][1]) < 10:  # y坐标相差不超过10则被认为是同一行
            tmp_line.append(data_all[i])
        else:
            if tmp_line:
                data_lines.append(tmp_line)
            tmp_line = []
            tmp_line.append(data_all[i])
    data_lines.append(tmp_line)

    value = ""
    for line in data_lines:
        line_value = ""
        for data in line:
            line_value += data[2].strip() + "  "
        if line_value.strip() != "":
           line_value += "\n"
        value += line_value
    return value

def get_min_width_height(blocks):
    '''
    @param blocks: 所有的单元格块
    @return: 最小的寛和高，用与辅助后面的合并单元格
    '''
    min_width = sys.maxsize
    for block in blocks:
        if block[1][0] - block[0][0] < min_width:
            min_width = block[1][0] - block[0][0]

    min_height = sys.maxsize
    for block in blocks:
        if block[1][1] - block[0][1] < min_height:
            min_height = block[1][1] - block[0][1]
    min_height = min_height/2
    return min_width, min_height

def run_tr(img_path, excel_path):
    '''
    运行对图片进行处理，然后运行tr
    :param img_path: 图片路径
    :return: 不返回，直接将数据写入表格文件
    '''
    # img_pil = Image.open(img_path)
    img_cv = cv2.imread(img_path)

    NORM_SIZE = 1600 # 图片大小都变换为1600
    height, width, channel = img_cv.shape
    scale = max(height / NORM_SIZE, width / NORM_SIZE)

    new_width = int(width / scale + 0.5)
    new_height = int(height / scale + 0.5)
    img_cv = cv2.resize(img_cv, (new_width, new_height))
    blocks = split_pic.split_pic(img_cv)
    min_width, min_height = get_min_width_height(blocks)

    img_cv = remove_seal.remove_seal(img_cv)
    img_pil = Image.fromarray(cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB))
    img_pil = img_pil.convert("L")

    excel_f = xlwt.Workbook()
    sheet = excel_f.add_sheet('sheet', cell_overwrite_ok=True)
    for i in range(50):
        col = sheet.col(i)  # xlwt中是行和列都是从0开始计算的
        col.width = 256 * 4

    block = blocks[0]

    cur_width = block[1][0] - block[0][0]
    cur_rows = int(cur_width / min_width)

    cur_height = block[1][1] - block[0][1]
    cur_lines = int(cur_height / min_height)

    region = img_pil.crop([block[0][0], block[0][1], block[1][0], block[1][1]])
    ocr_results = tr.run(region, flag=tr.FLAG_RECT)  # 运行tr，获得带位置的ocr结果
    value = get_value(ocr_results)
    sheet.write_merge(0, cur_lines-1, 0, cur_rows-1, value)
    line = cur_lines
    row = cur_rows
    for i in range(1, len(blocks)):
        block = blocks[i]
        cur_width = block[1][0] - block[0][0]
        cur_rows = int(cur_width / min_width)
        cur_height = block[1][1] - block[0][1]
        cur_lines = int(cur_height / min_height)

        if blocks[i][0][1] > blocks[i-1][0][1]:
            row = 0
            line += cur_lines

        row += cur_rows
        region = img_pil.crop([block[0][0], block[0][1], block[1][0], block[1][1]])
        ocr_results = tr.run(region, flag=tr.FLAG_RECT) #运行tr，获得带位置的ocr结果
        value = get_value(ocr_results)
        sheet.write_merge(line-cur_lines, line-1, row - cur_rows, row -1, value, xlwt.easyxf('align: wrap on'))  # 第1行第1列

    excel_f.save(excel_path)

if __name__ == '__main__':
    run_tr("invoice.png", "invoice.xls")
