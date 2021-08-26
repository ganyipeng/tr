# -*- coding: utf-8 -*- 
# @Time 2021/8/26 13:53

import BlockRowsAndOcrValuesToRows
# import tr


def get_ocr_values_from_pil_img(pil_img):
    # ocr_values = tr.run(pil_img, flag=tr.FLAG_RECT)  # 运行tr，获得带位置的ocr结果
    ocr_values = BlockRowsAndOcrValuesToRows.get_fake_ocr_values_data()
    return ocr_values

