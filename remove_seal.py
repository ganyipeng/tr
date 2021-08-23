import cv2
import numpy as np

def cnt_area(cnt):
    area = cv2.contourArea(cnt)
    return area

def my_threshold(img, thresh, min):
    '''
    @param img: 印章所在的图片区域
    @param thresh: 二值化的阈值
    @param min: 低于阈值的点被设置的颜色
    @return: 去除印章之后的二值图片
    '''
    ret, th = cv2.threshold(img, thresh, min, cv2.THRESH_BINARY)
    th1 = min - th
    th1 = 255 - th1
    return th1

def find_seal(image, low_range, high_range, thresh):
    '''
    @param image: 图片
    @param low_range: 色域的下界
    @param high_range: 色域的上界
    @param thresh: 用于删除印章的阈值
    @return: 印章所在区域和该区域删除印章之后的图片
    '''
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    th = cv2.inRange(hsv_image, low_range, high_range)
    index1 = th == 255
    img = np.zeros(image.shape, np.uint8)
    img[:, :] = (255, 255, 255)
    img[index1] = image[index1]  # (0,0,255)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(~gray, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours.sort(key=cnt_area, reverse=True)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    seal_image = image[y:y + h, x:x + w]
    b, g, r = cv2.split(seal_image)

    g_b_img = my_threshold(r, thresh, 220)
    r_img = my_threshold(r, thresh, 100)
    seal_image[:, :, 0] = g_b_img
    seal_image[:, :, 1] = g_b_img
    seal_image[:, :, 2] = r_img

    return [x,y,w,h], seal_image



def remove_seal(image):
    '''
    @param image: 原图
    @return: 抹去印章的图片
    '''
    # image=cv2.imread(r"file.jpg")
    # 上面那个印章的色域
    low_range = np.array([0, 80, 150])
    high_range = np.array([50, 255, 205])
    [x,y,w,h], seal_region = find_seal(image, low_range, high_range, 150)
    image[y:y + h, x:x + w ] = seal_region

    #下面那个印章的色域
    low_range = np.array([150, 123, 150])
    high_range = np.array([180, 255, 255])
    [x, y, w, h], seal_region = find_seal(image, low_range, high_range, 160)
    image[y:y + h, x:x + w] = seal_region

    return image