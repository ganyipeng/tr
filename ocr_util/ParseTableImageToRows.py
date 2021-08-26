# -*- coding: utf-8 -*- 
# @Time 2021/8/26 11:28

import BlockRowsAndOcrValuesToRows
import ImageCommonProcess
import OcrCommonProcess
import BlocksCommonProcess


def run(img_path):
    # step1: get pil img from img path
    # img_path = 'gbl.png'
    bin_pil_img = ImageCommonProcess.gray_bin_and_return_pil_img(img_path)

    # step2: get ocr values from bin pil img
    ocr_values = OcrCommonProcess.get_ocr_values_from_pil_img(bin_pil_img)

    # step3: get blocks from
    block_rows = BlocksCommonProcess.get_block_rows_from_bin_pil_img(bin_pil_img)

    # step4: get rows
    rows = BlockRowsAndOcrValuesToRows.run(block_rows, ocr_values)

    return rows


if __name__ == '__main__':
    rows = run('gbl.png')
    print(rows)
