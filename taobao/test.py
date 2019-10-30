'''
@Description: 
@Author: Shalor
@Date: 2019-10-30 11:27:07
'''
# '''
# @Description: 
# @Author: Shalor
# @Date: 2019-10-30 09:53:10
# '''
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys

# # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# # #get直接返回，不再等待界面加载完成
# # desired_capabilities = DesiredCapabilities.CHROME
# # desired_capabilities["pageLoadStrategy"] = "none"
# options = webdriver.ChromeOptions()
# # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# browser = webdriver.Chrome(options=options)
# wait = WebDriverWait(browser, 10)

# def search():
#     browser.get('http://www.taobao.com')
#     input = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
#     )
#     # submit = wait.until(
#     #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > button"))
#     # )
#     input.send_keys('美食')
#     input.send_keys(Keys.ENTER)

# def main():
#     search()

# if __name__ == "__main__":
#     main()
    

import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

dirver = webdriver.Chrome()
dirver.get(
    'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3D875.7931836%252FB.a2226mz.4.66144265Vdg7d5%26t%3D20110530')
# 这里是为了等待手机扫码登录, 登录后回车即可
input("请回车登录")
dictCookies = dirver.get_cookies()
jsonCookies = json.dumps(dictCookies)
# 登录完成后,将cookies保存到本地文件
with open("cookies_tao.json", "w") as fp:
    fp.write(jsonCookies)