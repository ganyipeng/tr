import cv2
import numpy

'''
获取表格中每一条竖线的x坐标
'''
def bin_img(img:'numpy.ndarray'):
    """
    对图像进行二值化处理
    :param img: 传入的图像对象（numpy.ndarray类型）
    :return: 二值化后的图像
    """
    ret,binImage=cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)
    return binImage

def gray_img(img:'numpy.ndarray'):
    """
    对读取的图像进行灰度化处理
    :param img: 通过cv2.imread(imgPath)读取的图像数组对象
    :return: 灰度化的图像
    """
    grayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return grayImage
    pass

def erode_img(img,kernel_args=(2,2),iterations=1):
    """
    对图像进行腐蚀
    @param kernel_args 卷积核参数（2，2）
    @param interations erode的迭代次数
    """
    kernel = numpy.ones(kernel_args, numpy.uint8)
    return cv2.erode(img, kernel,iterations=iterations)

def dilate_img(img, kernal_args:tuple, iterations:int):
    """
    dilate image
    @param kernel_args 卷积核参数（2，2）
    @param interations dilate的迭代次数
    """

    kernel = numpy.ones(kernal_args, numpy.uint8)
    return cv2.dilate(img, kernel,iterations=iterations)

def get_row_x(img):
    """
    先对图片做各种变换，使图片只剩表格的竖线，然后返回竖线的x坐标
    """
    img = gray_img(img)
    img = bin_img(img)
    img = erode_img(img, (2, 1), 40)
    img = dilate_img(img, (2, 2), 1)
    cv2.imshow("", img)
    cv2.waitKey(0)
    x_dict = {} # 对很多行进行取样，统计在竖线上的x坐标
    for x in range(0, img.shape[0], 50):  #每隔50个像素点进行一行取样
        for y in range(img.shape[1]):  # 遍历这一行
            if img[x][y] > 100: # 如果遇到了竖线
                flag = True
                for key in x_dict.keys():
                    if abs(y-key) < 10: #如果这条竖线上已经有x坐标被找到了，就在那个x坐标的统计上加一
                        x_dict[key]+=1
                        flag = False
                if flag: # 如果这条竖线上还没有 x 坐标被找到，就加一个新的项
                    x_dict[y] = 1
    row_x = [] # 统计在竖线上的x坐标
    for key in x_dict.keys():
        if x_dict[key] > img.shape[0]/50 * 1.5: #如果超过取样数的1.5倍，则说明这个x坐标是竖线的
            row_x.append(key)

    return row_x
