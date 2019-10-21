'''
@Description: 
@Author: Shalor
@Date: 2019-10-21 15:45:27
'''
from urllib.error import URLError
from urllib.request import urlopen
import urllib

import re
import pymysql
import ssl

from pymysql import Error

import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def decode_page(page_bytes, charsets=('utf-8',)):
    """通过指定的字符集对页面进行解码(不是每个网站都将字符集设置为utf-8)"""
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html


def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
    """获取页面的HTML代码(通过递归实现指定次数的重试操作)"""
    page_html = None
    try:
        page_html = decode_page(urlopen(seed_url).read(), charsets)
    except URLError:
        # logging.error('URL:', error)
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times - 1,
                                 charsets=charsets)
    return page_html


def get_latest_page(page_html, pattern_str, pattern_ignore_case=re.I):
    """获取漫画最新的话数"""
    pattern_regex = re.compile(pattern_str, pattern_ignore_case)
    return pattern_regex.findall(page_html) if page_html else []


def get_last_index(s):
    L = len(s)
    index = L-1-s[::-1].find('"', 1)
    return s[index+1:-1]


# def main():
#     pass


if __name__ == "__main__":
    # 解析海贼王漫画网站
    html_page = get_page_html("https://manhua.fzdm.com/02/")

    # 获取海贼王所有的话数，并将其以列表形式返回
    pattern_str = r'<li class="pure-u-1-2 pure-u-lg-1-4"><a href=".+?/"'
    url_list = get_latest_page(html_page, pattern_str)
    url_list = [get_last_index(x) for x in url_list]
    # print(url_list)
    # print(len(url_list))

    # 将获得的所有的话数，加上前缀获得picture所在的页面
    for index in range(1):
        page_index = 0
        while True:
            
            url = "https://manhua.fzdm.com/02/"+url_list[index]+"index_"+str(page_index)+".html"
            # print(url)
            picture_html = get_page_html(url)
            picture_pattern = r'var mhurl=".*?\.jpg"'
            picture_url_list = get_latest_page(picture_html,picture_pattern)
            # print(picture_url_list)
            picture_url_part = picture_url_list[0][11:-1]
            full_picture_url = ""
            if picture_url_part[:4] in ["2016","2017","2018","2019"]:
                full_picture_url = "http://p1.manhuapan.com/"+picture_url_part
            else:
                full_picture_url = "http://p0.manhuapan.com/"+picture_url_part
            urllib.request.urlretrieve(full_picture_url, "999.jpg")
            page_index += 1
            break
            

    # urllib.request.urlretrieve("http://p0.manhuapan.com/2/Vol_030/008ao.jpg", "local-filename.jpg")
    