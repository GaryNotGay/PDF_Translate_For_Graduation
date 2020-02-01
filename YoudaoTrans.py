# -*- coding: utf-8 -*-

# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Jan 31,2020
# @describe:  Use YouDao-API to translate
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# Based On YouDao AI Open Platform official Python3 Demo
# https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html

import sys
import uuid
import time
import json
import hashlib
import requests
import datetime
from importlib import reload
reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '0734916a664b7ae2' #ID
APP_SECRET = 'GtM75ZrMTGhweyl4vtcC2XyVOhTMTXso' #KEY


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def find_translation_start(text):
    for index in range(0, len(text)-10):
        if text[index-1: index+12] == "\"translation\"":
            return index

def find_translation_end(text):
    for index in range(0, len(text)-10):
        if text[index-1: index+10] == "\"errorCode\"":
            return index


def connect(q, language, Is2language):
    try:
        data = {}
        data['from'] = 'auto'
        if language == 1:
            data['to'] = 'en'
        else:
            data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = do_request(data)
        responsetext = response.content.decode("utf-8")
        index_start = find_translation_start(responsetext)
        index_end = find_translation_end(responsetext)

        return_text = ''
        if Is2language:
            return_text = q
        return_text += responsetext[index_start + 15: index_end - 4]
        if Is2language:
            return_text += '\n'
        return return_text

    except BaseException as err:
        error_text = 'YouDaoError' + err
        return error_text
