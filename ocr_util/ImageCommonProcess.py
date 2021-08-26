# -*- coding: utf-8 -*- 
# @Time 2021/8/26 13:10

from PIL import Image
import cv2
import numpy

MAX_SIZE = 1600 # 图片的大小最好不超过 1600


def resize_image_from_img_path_to_array(img_path):
    pil_img = resize_image_from_img_path_to_pil_img(img_path)
    return pil_img_to_array(pil_img)


def resize_image_from_img_path_to_pil_img(img_path):
    img_pil = Image.open(img_path)
    return resize_pil_img(img_pil)


def resize_pil_img(img_pil):
    scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)
    new_width = int(img_pil.width / scale + 0.5)
    new_height = int(img_pil.height / scale + 0.5)
    img_pil = img_pil.resize((new_width, new_height), Image.ANTIALIAS)
    return img_pil


def pil_img_to_array(pil_img):
    return numpy.asarray(pil_img)


def resize_gray_bin_and_return_pil_img(img_path):
    bin_array = resize_gray_bin_and_return_array(img_path)
    bin_pil_img = Image.fromarray(bin_array.astype('uint8'))
    return bin_pil_img


def resize_gray_bin_and_return_array(img_path):
    array_of_img = resize_image_from_img_path_to_array(img_path)
    gray_array = get_gray_array(array_of_img)
    bin_array = get_bin_array(gray_array)
    return bin_array


def gray_bin_and_return_pil_img(img_path):
    bin_array = gray_bin_and_return_array(img_path)
    bin_pil_img = Image.fromarray(bin_array.astype('uint8'))
    return bin_pil_img


def gray_bin_and_return_array(img_path):
    gray_array = get_gray_array(numpy.asarray(Image.open(img_path)))
    bin_array = get_bin_array(gray_array)
    return bin_array


# gray process: ndarray -> ndarray
def get_gray_array(init_ndarray: 'numpy.ndarray'):
    gray_ndarray = cv2.cvtColor(init_ndarray, cv2.COLOR_BGR2GRAY)
    return gray_ndarray


# binary process: ndarray -> ndarray
def get_bin_array(img: 'numpy.ndarray'):
    ret, bin_image=cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    return bin_image


# show im('numpy.ndarray')
def show_image_by_ndarray(im_ndarray):
    im = Image.fromarray(im_ndarray.astype('uint8'))
    im.show()

# img = numpy.asarray(im)  # init image
#     im_gray = gray_img(img)  # gray image
#     # show(im_gray)
#     im_bin = bin_img(im_gray)  # bin image


def test():
    pil_img = resize_gray_bin_and_return_pil_img('bazirou.png')
    pil_img.show()


if __name__ == '__main__':
    test()