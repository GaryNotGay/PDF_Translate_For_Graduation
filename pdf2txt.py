# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Jan 31,2020
# @describe:  A way of achieve PDF to TXT
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

import re
import sys
import importlib
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed

def parse(in_path, out_path, start_num, end_num):
    fp = open(in_path, 'rb') # 以二进制读模式打开#
    praser = PDFParser(fp) # 用文件对象来创建一个pdf文档分析器
    doc = PDFDocument(praser) # 创建一个PDF文档
    praser.set_document(doc)# 连接分析器 与文档对象

    if start_num == 0 and end_num == 0:
        mode = 1
    elif start_num != 0 and end_num == 0:
        mode = 2
    elif start_num != 0 and end_num != 0:
        mode = 3

    temp_num = 0
    if not doc.is_extractable: # 检测文档是否提供txt转换，不提供就忽略
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager() # 创建PDf 资源管理器 来管理共享资源
        laparams = LAParams() # 创建一个PDF设备对象
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)# 创建一个PDF解释器对象

        for page in PDFPage.create_pages(doc): # 循环遍历列表，每次处理一个page的内容 其中doc.get_pages()获取page列表
            if mode == 2:
                temp_num += 1
                if temp_num < start_num:
                    continue
                elif temp_num > start_num:
                    break
            elif mode == 3:
                temp_num += 1
                if temp_num < start_num:
                    continue
                elif temp_num > end_num:
                    break

            interpreter.process_page(page) # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)): #需要写出编码格式 解决\u8457\u5f55\u683c\u5f0f\uff1a\u67cf\u6167乱码
                      with open(out_path, 'a', encoding = 'utf-8') as out_txt:
                             results = x.get_text()
                             #print(results)
                             out_txt.write(results + '\n')
    return
#parse(in_path)

