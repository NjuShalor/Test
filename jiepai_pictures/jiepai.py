'''
@Description: 
@Author: Shalor
@Date: 2019-10-29 11:13:36
'''
import os
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from config import *
import pymongo
from hashlib import md5
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page_index(offset,keyword):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'cookie': 'tt_webid=6752776204430558728; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6752776204430558728; csrftoken=3e9017d2f3cc9ec4232b5c7e84910bdb; s_v_web_id=2eed892afd409f86752e6eef32eb182e; __tasessionId=ofb4zozv31572331011042',
    }
    data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time()),
    }
    url = 'https://www.toutiao.com/api/search/content/?'+ urlencode(data)
    
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None


def parse_page_index(html):
    print(html.count('article_url'))
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get("article_url")


def get_page_detail(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'cookie': 'tt_webid=6752776204430558728; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6752776204430558728; csrftoken=3e9017d2f3cc9ec4232b5c7e84910bdb; s_v_web_id=2eed892afd409f86752e6eef32eb182e; __tasessionId=ofb4zozv31572331011042',
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求详情页出错",url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    content_pattern = re.compile(r'content.*?groupId',re.S)
    content_part = re.search(content_pattern,html)
    if content_part:
        picture_pattern = re.compile(r'http:\\u002F.*?;',re.S)
        picture_urls = re.findall(picture_pattern,content_part.group())
        picture_urls = [item[:-7].encode('utf-8').decode('unicode_escape') for item in picture_urls]
        for picture in picture_urls:
            download_image(picture)
        return {
            'title':title,
            'url':url,
            'images':picture_urls
        }
    else:
        return {
            'title':title,
            'url':url,
            'images':[]
        }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print("存储到MongoDB成功",result)
        return True
    return False   

def download_image(url):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    #     'cookie': 'tt_webid=6752776204430558728; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6752776204430558728; csrftoken=3e9017d2f3cc9ec4232b5c7e84910bdb; s_v_web_id=2eed892afd409f86752e6eef32eb182e; __tasessionId=ofb4zozv31572331011042',
    # }
    print("正在下载",url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print("请求图片出错")
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'.jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            # if result:save_to_mongo(result)


if __name__ == "__main__":
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main,groups)
