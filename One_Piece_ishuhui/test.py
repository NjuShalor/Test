# '''
# @Description: 
# @Author: Shalor
# @Date: 2019-11-05 20:06:02
# '''
# import os
# import time
# import requests
# from selenium import webdriver
# from lxml import etree


# def down_comic_by_url(url,last_chapter=True):
#     '''
#     :param url: 腾讯动漫某动漫首页地址
#     :param lastChapter: True是否最新话|False全本
#     :return:
#     '''
#     print(url)
#     print(last_chapter)
#     headers = {
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
#         }
#     part_url = "http://ac.qq.com"
#     res = requests.get(url, headers=headers)
#     html=res.content.decode()
#     el = etree.HTML(html)
#     if(last_chapter):
#         # 仅获取最新一话
#         span = el.xpath('//*[@id="chapter"]/div[2]/ol[1]/li[last()]/p[last()]/span[last()]')
#         print(span)
#         list_title = span[0].xpath("./a/@title")[0].replace(' ', '').split('：')
#         if list_title[1].startswith(('第', '序')):
#             save_chapter_to_file(part_url + span[0].xpath("./a/@href")[0], list_title[0], list_title[1])
#         # 仅获取最新一话
#     else:
#         # 获取全本
#         li_list = el.xpath('//*[@id="chapter"]/div[2]/ol[1]/li')
#         print(len(li_list))
#         for li in li_list:
#                 for p in li.xpath("./p"):
#                     for span in p.xpath("./span[@class='works-chapter-item']"):
#                         list_title = span.xpath("./a/@title")[0].replace(' ', '').split('：')
#                         if list_title[1].startswith(('第', '序')):
#                             save_chapter_to_file(part_url + span.xpath("./a/@href")[0], list_title[0], list_title[1])


# def save_chapter_to_file(url,path1,path2):
#     '''
#     :param url: 章节地址
#     :param path1:
#     :param path2:
#     :return:
#     '''
#     #漫画名称目录
#     print(url)
#     print(path1)
#     print(path2)
#     path=os.path.join(path1)
#     if not os.path.exists(path):
#         os.mkdir(path)
#     #章节目录
#     path=path+'/'+path2
#     if not os.path.exists(path):
#         os.mkdir(path)
#     chrome=webdriver.Chrome()
#     chrome.maximize_window()
#     chrome.get(url)
#     time.sleep(4)
#     # 定位到img,过滤掉广告图片
#     imgs = chrome.find_elements_by_xpath("//div[@id='mainView']/ul[@id='comicContain']/li[not(@class)]//img")
#     print(imgs)
#     totalheight = 0
#     for i in range(0, len(imgs)):
#         # 循环等待直到Ajax图片返回
#         while True:
#             image = imgs[i].get_attribute("src")
#             if(image.endswith("pixel.gif")==False):
#                 break
#             time.sleep(2)

#         filename = imgs[i].get_attribute("data-pid")
#         imgheight = int(imgs[i].get_attribute("data-h"))
#         print(imgs[i].get_attribute("src") + " height:" + str(imgheight))

#         js = "document.getElementById('mainView').scrollTop=" + str(totalheight)  # 按图片高度滚动
#         chrome.execute_script(js)
#         if(i==0):
#             totalheight = totalheight + 115 # ad广告高度
#         totalheight = totalheight + imgheight + 31 # 间距高度

#         with open(path+'/'+filename+'.jpg', 'wb') as f:
#             f.write(requests.get(imgs[i].get_attribute("src")).content)

#     chrome.close()
#     print(path2+'下载完成')

# if __name__ == '__main__':
#     # One Piece 海贼王
#     # down_comic_by_url('http://ac.qq.com/Comic/ComicInfo/id/505430')
#     save_chapter_to_file('http://ac.qq.com/ComicView/index/id/505430/cid/1','航海王','第1话ROMANCE DAWN')

import os
if not os.path.exists('./海贼王/第一话/'):
    os.makedirs('./海贼王/第一话/')