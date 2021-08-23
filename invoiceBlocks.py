# -*- coding: utf-8 -*- 
# @Time 2021/8/19 14:19
import cv2
from PIL import Image
import numpy

# code from：https://blog.csdn.net/weixin_42194239/article/details/91975662


# gray process
def gray_img(img: 'numpy.ndarray'):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_image


# binary process
def bin_img(img: 'numpy.ndarray'):
    ret, bin_image=cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    return bin_image


# erode process
def erode_img(img, kernel_args=(2, 2), iterations=1):
    kernel = numpy.ones(kernel_args, numpy.uint8)
    return cv2.erode(img, kernel, iterations=iterations)


# dilate up process
def dilate_img_up(img, iterations: int):
    kernel = numpy.array([
        [0],
        [1],
        [1]
    ], dtype=numpy.uint8)
    return cv2.dilate(img, kernel, iterations=iterations)


# dilate up process
def dilate_img_left(img, iterations: int):
    kernel = numpy.array([
        [0, 1, 1]
    ], dtype=numpy.uint8)
    return cv2.dilate(img, kernel, iterations=iterations)


def get_points(img_transverse, img_vertical):
    img = cv2.bitwise_and(img_transverse, img_vertical)
    return img


def get_replace_dict(arg_list):
    aa = arg_list.tolist()
    bb = [0] + aa[0:-1]
    cc = [x - bb[j] for j, x in enumerate(aa)]
    my_replace = {}
    v = 0
    for i, c in enumerate(cc):
        if i == 0 or c > 3:
            v = aa[i]
        my_replace[aa[i]] = v
    return my_replace


def update_nd_array_one_axis(nd_array_one_axis, replact_dict):
    list1 = nd_array_one_axis.tolist()
    list2 = [replact_dict[x] for x in list1]
    return list2


# distinct points
def distinct_x_and_y_list(x_list, y_list):
    xy_list = [[_x, y_list[_i]] for _i, _x in enumerate(x_list)]
    xy_result = []
    for xy in xy_list:
        if xy not in xy_result:
            xy_result.append(xy)
    return xy_result

# rows
def split_rows(xy_result):
    rows = [[[-1,-1]]]
    i = 0
    for xy in xy_result:
        if rows[-1][0][0] == xy[0]:
            rows[-1].append(xy)
        else:
            rows.append([xy])
    return rows[1:]


def filter_points(img_points):
    valid_points = numpy.where(img_points > 0)
    x_axis = valid_points[0]  # x axis is row line
    y_axis = valid_points[1]  # y axis is col line
    x_unique_sort = numpy.sort(numpy.unique(x_axis))
    y_unique_sort = numpy.sort(numpy.unique(y_axis))
    x_replace_dict = get_replace_dict(x_unique_sort)
    y_replace_dict = get_replace_dict(y_unique_sort)
    x_axis_align = update_nd_array_one_axis(x_axis, x_replace_dict)
    y_axis_align = update_nd_array_one_axis(y_axis, y_replace_dict)
    xy_result = distinct_x_and_y_list(x_axis_align, y_axis_align)
    rows = split_rows(xy_result)

    return rows


def get_blocks(rows):
    rows_len = len(rows)
    blocks = []
    for i in range(0, rows_len-1):
        x = rows[i][0][0]
        start_row = rows[i]
        end_row = rows[i+1]
        start_y = [p[1] for p in start_row]
        end_y = [p[1] for p in end_row]
        common_y = numpy.intersect1d(numpy.array(start_y), numpy.array(end_y)).tolist()
        # print('common_y', common_y)
        y_len = len(common_y)
        block_row = [[[common_y[j-1], x], [common_y[j], end_row[0][0]]] for j in range(1, y_len)]
        blocks.append(block_row)
    return blocks


def get_blocks_with_top_and_bottom(blocks, shape):
    width, height = shape
    x_left_top = blocks[0][0][0][0]
    y_left_top = 0
    x_right_top = blocks[0][-1][1][0]
    y_right_top = blocks[0][0][0][1]
    top_block = [[x_left_top, y_left_top], [x_right_top, y_right_top]]

    x_left_bottom = x_left_top
    y_left_bottom = blocks[-1][-1][1][1]
    x_right_bottom = x_right_top
    y_right_bottom = height
    bottom_block = [[x_left_bottom, y_left_bottom], [x_right_bottom, y_right_bottom]]

    blocks = [[top_block], *blocks, [bottom_block]]
    result = []
    for block in blocks:
        result = [*result, *block]

    return result


# show im('numpy.ndarray')
def show(im):
    im = Image.fromarray(im.astype('uint8'))
    im.show()


# test function
def parse(im):
    # im = Image.open(img_path)
    img = numpy.asarray(im)  # init image
    im_gray = gray_img(img)  # gray image
    # show(im_gray)
    im_bin = bin_img(im_gray)  # bin image

    iterations = 60
    img_horizontal_erode = erode_img(im_bin, (1, 2), iterations)  # get horizontal line image
    img_vertical_erode = erode_img(im_bin, (2, 1), iterations)  # get vertical line image
    img_horizontal_dilate = dilate_img_up(img_vertical_erode, iterations)  # add pix at top of the img_vertical_erode
    img_vertical_dilate = dilate_img_left(img_horizontal_erode, iterations)  # add pix at left of the img_horizontal_erode
    show(img_horizontal_dilate+img_vertical_dilate)
    img_points = get_points(img_horizontal_dilate, img_vertical_dilate)
    points_rows = filter_points(img_points)
    blocks = get_blocks(points_rows)
    blocks = get_blocks_with_top_and_bottom(blocks, im_bin.shape)

    # print('blocks', blocks)
    # for i,row in enumerate(blocks):
    #     print("第",i+1,"行 共",len(row),"块，坐标如下所示：")
    #     for j,block in enumerate(row):
    #         print("\t第",j+1,"块区域",block)
    #     print()

    return blocks



# test()

# blocks 18 [[[31, 131], [67, 214]], [[67, 131], [528, 214]], [[528, 131], [548, 214]], [[548, 131], [896, 214]], [[31, 214], [258, 380]], [[258, 214], [366, 380]], [[366, 214], [420, 380]], [[420, 214], [506, 380]], [[506, 214], [595, 380]], [[595, 214], [723, 380]], [[723, 214], [769, 380]], [[769, 214], [896, 380]], [[31, 380], [258, 409]], [[258, 380], [896, 409]], [[31, 409], [67, 488]], [[67, 409], [528, 488]], [[528, 409], [548, 488]], [[548, 409], [896, 488]]]
#
# 第 1 行 共 4 块，坐标如下所示：
# 	第 1 块区域 (32, 131, 67, 215)
# 	第 2 块区域 (67, 131, 526, 215)
# 	第 3 块区域 (526, 131, 548, 215)
# 	第 4 块区域 (548, 131, 896, 215)
#
# 第 2 行 共 8 块，坐标如下所示：
# 	第 1 块区域 (32, 215, 258, 380)
# 	第 2 块区域 (258, 215, 366, 380)
# 	第 3 块区域 (366, 215, 420, 380)
# 	第 4 块区域 (420, 215, 506, 380)
# 	第 5 块区域 (506, 215, 595, 380)
# 	第 6 块区域 (595, 215, 723, 380)
# 	第 7 块区域 (723, 215, 769, 380)
# 	第 8 块区域 (769, 215, 896, 380)
#
# 第 3 行 共 2 块，坐标如下所示：
# 	第 1 块区域 (32, 380, 258, 410)
# 	第 2 块区域 (258, 380, 896, 410)
#
# 第 4 行 共 4 块，坐标如下所示：
# 	第 1 块区域 (32, 410, 67, 488)
# 	第 2 块区域 (67, 410, 526, 488)
# 	第 3 块区域 (526, 410, 548, 488)
# 	第 4 块区域 (548, 410, 896, 488)