'''
@Description: 
@Author: Shalor
@Date: 2019-11-05 16:13:30
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# options = webdriver.ChromeOptions()
# # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# # options.add_argument("--headless")
# browser = webdriver.Chrome(options=options)

browser = webdriver.Chrome()

# cookies = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': '__AC__=1; pgv_pvi=3453271040; RK=/ESMNND8Gx; ptcz=2278ea6a48ee77ccb3d9f5cc1b58880cb9801c89712994a480f05cb97b0d66cb; ptui_loginuin=869546825; tvfe_boss_uuid=9af1438adf21542f; pgv_pvid=5181133629; ts_uid=6827243640; theme=dark; readLastRecord=%5B%5D; o_cookie=869546825; ts_refer=www.ishuhui.com/comics/anime/1; nav_userinfo_cookie=; pgv_info=ssid=s5362020456; roastState=2; readRecord=%5B%5B505430%2C%22%E8%88%AA%E6%B5%B7%E7%8E%8B%22%2C1%2C%22%E7%AC%AC1%E8%AF%9D%20ROMANCE%20DAWN%20%E5%86%92%E9%99%A9%E7%9A%84%E5%BA%8F%E5%B9%95%22%2C1%5D%5D; ts_last=ac.qq.com/ComicView/index/id/505430/cid/1',
#     'Host': 'ac.qq.com',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': 1,
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
#     }
# cookies = {
#     '__AC__':1,
#     'pgv_pvi':3453271040,
#     'RK':'/ESMNND8Gx',
#     'ptcz':'2278ea6a48ee77ccb3d9f5cc1b58880cb9801c89712994a480f05cb97b0d66cb',
#     'ptui_loginuin':869546825,
#     'tvfe_boss_uuid':'9af1438adf21542f',
#     'pgv_pvid':5181133629,
#     'ts_uid':6827243640,
#     'theme':'dark',
#     'readLastRecord':'%5B%5D',
#     'o_cookie':869546825,
#     'ts_refer':'www.ishuhui.com/comics/anime/1',
#     'nav_userinfo_cookie':'',
#     'pgv_info':'s5362020456',
#     'ssid':'s5362020456',
#     'roastState':2,
#     'readRecord':'%5B%5B505430%2C%22%E8%88%AA%E6%B5%B7%E7%8E%8B%22%2C1%2C%22%E7%AC%AC1%E8%AF%9D%20ROMANCE%20DAWN%20%E5%86%92%E9%99%A9%E7%9A%84%E5%BA%8F%E5%B9%95%22%2C1%5D%5D',
#     'ts_last':'ac.qq.com/ComicView/index/id/505430/cid/1'
# }

def get_detail(url):
    browser.get(url)
    # browser.add_cookie(cookies)
    # title = browser.find_element_by_css_selector('#comicTitle > span.title-comicHeading')
    # print(title.text)
    # images = browser.find_elements_by_css_selector('#comicContain > li > img')
    # for item in images:
    #     print(item.get_attribute('src'))
    # return browser.page_source

    # browser.execute_script('alert("To Bottom")')
    time.sleep(30)
    return browser.page_source


def main(page):
    url = 'https://ac.qq.com/ComicView/index/id/505430/cid/'+str(page)
    html = get_detail(url)
    with open('./html.txt','w',encoding='utf-8') as f:
        f.write(html)
        f.close()

    

if __name__ == "__main__":
    main(1)