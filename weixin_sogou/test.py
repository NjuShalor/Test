'''
@Description: 
@Author: Shalor
@Date: 2019-11-05 14:10:10
'''
import json
import time
import re
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pyquery import PyQuery as pq
import pymongo

options = webdriver.ChromeOptions()
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=options)

base_url = 'https://weixin.sogou.com/weixin?'
keyword = '风景'


def get_html(url):
    browser.get(url)
    print(browser.page_source)

def main():
    data = {
        'query':keyword,
        'type':2,
        'page':1
        }
    queries = urlencode(data)
    url = base_url + queries
    get_html(url)

if __name__ == "__main__":
    main()