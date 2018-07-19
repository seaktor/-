# coding: utf8
'''
    @Author: LYF
    @Date: 2018-07-02
    官方链接：
           http://api.fanyi.baidu.com/api/trans/product/index
           
'''
 
import http.client
import hashlib
import json
import urllib
import random
 
def baidu_translate(content):
    appid = '20180702000181982'
    secretKey = 'PRsdcSMA4A_cewFhTXNt'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'en' # 源语言
    toLang = 'zh'   # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
 
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return dst # 打印结果
    except Exception as e:
        print(e)

