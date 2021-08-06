import fitz
from runtr import run_tr
import csv
import os

def writecsv(res_data, res_file):
    with open(res_file, "w") as res_f:
        writer = csv.writer((res_f))
        for line in res_data:
            writer.writerow(line)

def pdf_image(pdfPath,imgPath,zoom_x,zoom_y):
    '''
    用 fitz 对PDF进行处理
    :param pdfPath:
    :param imgPath:
    :param zoom_x: 和下面的 zoom_y 一起控制输出图片的质量
    :param zoom_y:
    :return:
    '''
    pdf = fitz.open(pdfPath)
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(0)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(imgPath+str(pg)+".png")
        #pm.writePNG(imgPath)
        res_data = run_tr(imgPath+str(pg)+".png") # 运行tr获得表格格式的数据
        writecsv(res_data, imgPath+str(pg)+".csv")



if __name__ == '__main__':
    pdf_path = "file1.pdf"
    img_path = pdf_path.replace(".pdf", "/") # 所有图片存储在pdf同名的文件夹下
    folder = os.path.exists(img_path)
    if not folder:
        os.makedirs(img_path)
    pdf_image(pdf_path,img_path,4 ,4)
