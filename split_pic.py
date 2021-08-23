import cv2
import numpy as np
import sys


def get_transverse(binary):
    '''
    @param binary: 二值化之后的图像
    @return: 只剩横线的图片
    '''
    rows, cols = binary.shape
    scale = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    img_transverse = cv2.dilate(eroded, kernel, iterations=1)
    # cv2.imshow("", img_transverse)
    # cv2.waitKey()
    return img_transverse

def get_vertical(binary):
    '''
        @param binary: 二值化之后的图像
        @return: 只剩竖线的图片
        '''
    rows, cols = binary.shape
    scale = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    img_vertical = cv2.dilate(eroded, kernel, iterations=1)
    # cv2.imshow("表格竖线展示：",img_vertical)
    # cv2.waitKey(0)
    return img_vertical

def is_same_points(point1, point2):
    '''
    @param point1:
    @param point2:
    @return: 判断两个点是否相同，相同返回True
    '''
    if abs(point1[0] - point2[0]) < 5 and abs(point1[1] - point2[1]) < 5:
        return True
    return False

def clean_points(points):
    '''
    @param points: 图片上所有白点的像素位置
    @return: 删除重复的点
    '''
    res_points = []
    count = len(points)
    for i in range(count-1):
        if points[i][0] == -1:
            continue
        res_points.append(points[i])
        for j in range(i+1, count):
            if is_same_points(points[i], points[j]):
                points[j] = [-1, -1]
    if points[count-1][0] != -1:
        res_points.append(points[count-1])
    return res_points

def add_four_corners(points, rows):
    '''
    @param points: 所有点
    @param rows: 图片的高度
    @return: 把图片的四个角加进去
    '''
    res_points = points
    left_up = [points[0][0], points[0][1]]
    for point in points:
        if point[0] <= left_up[0] and point[1] <= left_up[1]:
            left_up = [point[0], point[1]]

    right_up = [points[0][0], points[0][1]]
    for point in points:
        if point[0] >= right_up[0] and point[1] <= right_up[1]:
            right_up = [point[0], point[1]]

    left_down = [points[0][0], points[0][1]]
    for point in points:
        if point[0] <= left_down[0] and point[1] >= left_down[1]:
            left_down = [point[0], point[1]]

    right_down = [points[0][0], points[0][1]]
    for point in points:
        if point[0] >= right_down[0] and point[1] >= right_down[1]:
            right_down = [point[0], point[1]]

    left_up[1] = 0
    right_up[1] = 0
    left_down[1] = rows
    right_down[1] = rows
    # print(left_up)
    # print(right_up)
    # print(left_down)
    # print(right_down)
    res_points.append(left_up)
    res_points.append(right_up)
    res_points.append(left_down)
    res_points.append(right_down)
    return res_points

def norm_points(points):
    '''
    @param points: 所有点
    @return: 格式化后的点，让每一行的y坐标相等，每一列的x坐标相等
    '''
    count = len(points)
    for i in range(count-1):
        for j in range(i+1, count):
            if abs(points[j][0] - points[i][0]) < 5:
                points[j][0] = points[i][0]
            if abs(points[j][1] - points[i][1]) < 5:
                points[j][1] = points[i][1]


def find_down_point(index, points):
    '''
    @param index: 当前点的索引
    @param points: 所有点
    @return: 返回当前点下面的第一个点
    '''
    if index >= len(points) - 1:
        return [-1, -1]
    count_line = 0
    cur_y = points[index][1]
    for i in range(index+1, len(points)):
        if (points[i][1] - cur_y) > 5:
            cur_y = points[i][1]
            count_line += 1
        if count_line > 1:
            break
        if abs(points[i][0] - points[index][0]) < 5 and points[i][1] > points[index][1]:
            return points[i]
    return [-1, -1]


def find_right_points(index, points):
    '''
    @param index: 当前点的索引
    @param points: 所有的点
    @return: 返回和当前点一行的右边所有点
    '''
    right_points = []
    for i in range(index+1, len(points)):
        if points[i][0] > points[index][0] and abs(points[i][1] - points[index][1]) < 5:
            right_points.append(points[i])
        if abs(points[i][1] - points[index][1]) > 5:
            break
    return right_points

def find_point(point, points):
    '''
    @param point: 目标点
    @param points: 所有点
    @return: 在所有点中找到目标点，找到返回true
    '''
    for i in range(len(points)):
        if is_same_points(points[i], point):
            return True
    return False

def get_blocks(binary, points):
    '''
    @param binary: 二值化之后的图片
    @param points: 表格中所有的交点
    @return: 每一个单元格的框，每个框用左上和右下角的两个点表示
    '''
    rows, cols = binary.shape
    points = clean_points(points)
    points = add_four_corners(points, rows)
    norm_points(points)
    points = sorted(points, key=lambda x: (x[1], x[0]))
    # for point in points:
    #     print(point)

    count = len(points)
    blocks = []
    for i in range(count):
        down_point = find_down_point(i, points)
        if down_point[0] == -1:
            continue
        right_points = find_right_points(i, points)
        for right_point in right_points:
            right_down = [right_point[0], down_point[1]]
            if not find_point(right_down, points):
                continue
            # print(points[i])
            # print(right_point)
            # print(down_point)
            # print(right_down)
            # print("------------------")
            cur_block = []
            cur_block.append(points[i])
            cur_block.append(right_down)
            blocks.append(cur_block)
            break

    return blocks

def split_pic(image):
    # image = cv2.imread("file.jpg", 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    img_transverse = get_transverse(binary)
    img_vertical = get_vertical(binary)
    img_points = cv2.bitwise_and(img_transverse,img_vertical)
    img = img_vertical + img_transverse

    ys,xs = np.where(img_points>0)
    points = []
    for i in range(len(ys)):
        point = [xs[i], ys[i]]
        points.append(point)

    blocks = get_blocks(binary, points)
    return blocks