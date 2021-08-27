# -*- coding: utf-8 -*- 
# @Time 2021/8/26 13:53

from . import BlockRowsAndOcrValuesToRows
import tr
import sys, cv2, time, os
from PIL import Image, ImageDraw, ImageFont


def get_ocr_values_from_pil_img(pil_img):
    ocr_values = tr.run(pil_img, flag=tr.FLAG_RECT)  # 运行tr，获得带位置的ocr结果
    # ocr_values = BlockRowsAndOcrValuesToRows.get_fake_ocr_values_data()
    return ocr_values


def get_ocr_values_from_img_path(img_path):
    img_pil = Image.open(img_path)
    try:
        if hasattr(img_pil, '_getexif'):
            # from PIL import ExifTags
            # for orientation in ExifTags.TAGS.keys():
            #     if ExifTags.TAGS[orientation] == 'Orientation':
            #         break
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

    MAX_SIZE = 1600
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.ANTIALIAS)

    color_pil = img_pil.convert("RGB")
    gray_pil = img_pil.convert("L")

    t = time.time()
    n = 1
    for _ in range(n):
        tr.detect(gray_pil, flag=tr.FLAG_RECT)
    print("time", (time.time() - t) / n)

    ocr_values = tr.run(gray_pil, flag=tr.FLAG_ROTATED_RECT)

    return ocr_values

