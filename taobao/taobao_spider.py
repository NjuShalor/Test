'''
@Description: 
@Author: Shalor
@Date: 2019-10-30 09:53:10
'''
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# #get直接返回，不再等待界面加载完成
# desired_capabilities = DesiredCapabilities.CHROME
# desired_capabilities["pageLoadStrategy"] = "none"
options = webdriver.ChromeOptions()
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_argument("--headless")
# browser = webdriver.Chrome(options=options)

# 或者用无界面浏览器PhantomJS
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 20)
browser.set_window_size(1400,900)

def search():
    print("正在搜索第%s页"%(1))
    try:
        browser.get('https://www.taobao.com')
        browser.delete_all_cookies()
        with open("./cookies_tao.json", "r", encoding="utf8") as fp:
            ListCookies = json.loads(fp.read())
        for cookie in ListCookies:
            browser.add_cookie({
                'domain':'.taobao.com',
                'name':cookie['name'],
                'value':cookie['value'],
                'path':'/',
                'expires':None
            })
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        # submit = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > button"))
        # )
        input.send_keys(KEYWORD)
        input.send_keys(Keys.ENTER)

        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        search()

def next_page(page_number):
    """进行翻页操作"""
    print("正在搜索第%s页"%page_number)
    try:
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
            )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        # 进行判定是否翻页成功，即对高亮块中的元素和页码进行比对
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)

def main():
    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))
        print(total)
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print("出错了...")
    finally:
        browser.close()
if __name__ == "__main__":
    main()
    
