# coding: utf-8
import tr
import sys, cv2, time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

_BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASEDIR)


def test(img_path="gyp-line.png"):
    print("recognize", tr.recognize("imgs/line.png"))

    # img_path = "gyp-mul.png"
    # img_path = "gyp-line.png"
    # img_path = "imgs/name_card.jpg"

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

    img_draw = ImageDraw.Draw(color_pil)
    colors = ['red', 'green', 'blue', "purple"]

    t = time.time()
    n = 1
    for _ in range(n):
        tr.detect(gray_pil, flag=tr.FLAG_RECT)
    print("time", (time.time() - t) / n)

    results = tr.run(gray_pil, flag=tr.FLAG_ROTATED_RECT)

    rows = []
    for i, rect in enumerate(results):
        cx, cy, w, h, a = tuple(rect[0])
        rows.append([rect[1]])
        print(i, "\t", rect[1], rect[2])

    return {"rows":rows}

if __name__ == "__main__":
    test()
