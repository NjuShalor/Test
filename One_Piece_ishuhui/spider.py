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

keyword = '航海王'

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


def get_search_result(keyword):
    base_url = 'https://ac.qq.com/Comic/searchList?search='+keyword+'&page=1'
    browser.get(base_url)
    try:
        p_element = browser.find_element_by_css_selector('body > div.mod_958wr.mod_gbd.mod_wbg.mod_of.ma.mod_all_cata_wr > p.ma.mod_of.mod_bbd.all_total_num')
        print('搜索结果总共有%s条'%p_element.text)
        result_list = get_detail_search_result()
        page = 2
        while True:
            browser.get('https://ac.qq.com/Comic/searchList?search='+keyword+'&page='+str(page))
            temp_result = get_detail_search_result()
            if temp_result:
                result_list += get_detail_search_result()
                page += 1
            else:
                break
        print(result_list)

    except NoSuchElementException:
        print('查无结果')
        new_keyword = input('请重新输入想下载的漫画名:')
        get_search_result(new_keyword)

def get_detail_search_result():
    href_list = browser.find_elements_by_css_selector('body > div.mod_958wr.mod_gbd.mod_wbg.mod_of.ma.mod_all_cata_wr > ul > li > h4 > a')
    try:
        no_search_element = browser.find_element_by_css_selector('body > div.mod_958wr.mod_gbd.mod_wbg.mod_of.ma.mod_all_cata_wr > div.mod_960wr.mod_of.search_wr > span')
        return []
    except NoSuchElementException:
        result = []
        for item in href_list:
            title = item.get_attribute('title')
            href = item.get_attribute('href')
            result.append((title,href))
        return result

def main(page):
    url = 'https://ac.qq.com/ComicView/index/id/505430/cid/'+str(page)
    html = get_detail(url)


if __name__ == "__main__":
    get_search_result("火影忍者")
    # max_page = get_latest_page('https://ac.qq.com/Comic/comicInfo/id/505430')
    # print("Now downloading comics...")
    # for page in range(1, 21):
    #     try:
    #         main(page)
    #     except NoSuchElementException:
    #         pass
    # browser.close()
