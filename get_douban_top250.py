'''
@Description: 
@Author: Shalor
@Date: 2019-10-28 14:19:23
'''
import requests
import re

def get_one_html(url):
    response = requests.get(url)
    return response.text
    
def write_into_file(result):
    index,title,info,comment = result
    line = "\t".join([str(index),title.strip(),info.strip(),comment.strip()])
    line = line.replace("<br>","")
    line = line.replace("nbsp","")
    line = line.replace(";","")
    line = line.replace("\n","")
    line = line.replace("&","")
    line = line.replace("/","")
    line += "\n"
    with open("./douban_top250.txt","a",encoding="utf-8") as f:
        f.write(line)
        f.close()



def main(page_number):
    url = 'https://movie.douban.com/top250?start='+str(page_number)
    html = get_one_html(url)
    pattern = re.compile(r'<em class.*?>(\d*?)</em>.*?<div class="info">.*?<span class="title">(.*?)</span>.*?<div class="bd">.*?<p class="">(.*?)</p>.*?<span class="inq">(.*?)</span>',re.S)
    result = re.findall(pattern,html)
    for item in result:
        write_into_file(item)    

if __name__ == "__main__":
    for i in range(0,250,25):
        main(i)