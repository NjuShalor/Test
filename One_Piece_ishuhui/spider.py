'''
@Description: 
@Author: Shalor
@Date: 2019-11-05 16:13:30
'''
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from pyquery import PyQuery as pq
from selenium.common.exceptions import NoSuchElementException

# options = webdriver.ChromeOptions()
# # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# # options.add_argument("--headless")
# browser = webdriver.Chrome(options=options)

browser = webdriver.Chrome()
browser.maximize_window()


def get_detail(url):
    browser.get(url)
    time.sleep(2)
    title = browser.find_element_by_css_selector(
        '#comicTitle > span.title-comicHeading')
    title = title.text
    images = browser.find_elements_by_css_selector('#comicContain > li > img')
    time.sleep(2)
    base_js = "document.getElementById('mainView').scrollTop="
    total_height = 50
    for i in range(len(images)):
        src = images[i].get_attribute('src')
        height = int(images[i].get_attribute('data-h'))
        while src.endswith('pixel.gif'):
            time.sleep(2)
            src = images[i].get_attribute('src')
        download_picture(src, str(i+1), './海贼王/'+title+'/')
        total_height += height
        js = base_js + str(total_height)
        browser.execute_script(js)
    return browser.page_source


def get_latest_page(url):
    doc = pq(url=url)
    newest_element = doc(
        '#chapter > div.works-chapter-list-wr.ui-left > ol.chapter-page-new.works-chapter-list > li > p:last-child > span:last-child > a')
    print("海贼王最新一话是:", newest_element.text())
    href = newest_element.attr('href')
    index = len(href)-1-href[::-1].find('/')
    newest_page = int(href[index+1:])
    return newest_page


def download_picture(pic_url, pic_name, file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    image = requests.get(pic_url)
    with open(file_path+'/'+pic_name+'.jpg', 'wb') as f:
        f.write(image.content)


def main(page):
    url = 'https://ac.qq.com/ComicView/index/id/505430/cid/'+str(page)
    html = get_detail(url)


if __name__ == "__main__":
    max_page = get_latest_page('https://ac.qq.com/Comic/comicInfo/id/505430')
    print("Now downloading comics...")
    for page in range(1, 21):
        try:
            main(page)
        except NoSuchElementException:
            pass
    browser.close()
