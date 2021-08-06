# -*- coding: utf-8 -*- 
# @Time 2021/7/17 17:42

from pdf2docx import Converter
# https://www.osgeo.cn/python-docx/api/table.html#docx.table._Cell
from docx import Document

def pdf2json(docName):
    print(docName)
    pdfName = docName+'.pdf'
    print(pdfName)
    pdf = Converter(pdfName)

    docxName = docName+'.docx'
    print(docxName)
    pdf.convert(docxName)

    pdf.close()

    # Document 类，不仅可以新建word文档，也可以打开一个本地文档
    doc = Document(docxName)  # 想获取的文档文件名，这里是相对路径
    tables = doc.tables
    "class Sections(Sequence):"
    print(tables)

    table = tables[1]
    print(table)

    rows = table.rows
    print(rows)

    resultRows = []

    # rowNum = len(rows)
    for r in rows:
        cells = r.cells
        # cellNum = len(cells)
        resultRow = []
        for c in cells:
            resultRow.append(c.text)
        resultRows.append(resultRow)

    return {
        'rows': resultRows
    }
