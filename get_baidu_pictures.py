'''
@Description: 
@Author: Shalor
@Date: 2019-10-28 20:59:11
'''
import os
import re
import requests
from requests.exceptions import RequestException
from selenium import webdriver

def get_html_page(url):
    try:
        browser = webdriver.Chrome()
        browser.get(url)
        return browser.page_source
    except RequestException:
        print("请求%d出错"%url)
        return None

def main():
    url = 'https://www.ishuhui.com/comics/anime/1'
    html = get_html_page(url)
    pattern = re.compile(r'<a class="m-comics-num-link" url="(.*?)".*?<h3 class.*?>(.*?)</h3>',re.S)
    with open('./hh.txt','w',encoding='utf-8') as f:
        f.write(html)
        f.close()
    result = re.findall(pattern,html)
    print(result)

if __name__ == "__main__":
    main()