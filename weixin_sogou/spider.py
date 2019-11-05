'''
@Description: 
@Author: Shalor
@Date: 2019-11-01 16:19:20
'''
import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

base_url = 'https://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUV=00FF3E832498189B5DA45BF0C3AEB312; IPLOC=CN3201; SUID=68CAD4722E08990A000000005DAC6879; ld=Zkllllllll2NrpPZgzeoWqL7z4xNrpPitHF3zlllll9llllxVllll5@@@@@@@@@@; cd=1571580025&1ef1734bab09b08d3a75d4e601e33fdb; rd=Zkllllllll2NrpPZgzeoWqL7z4xNrpPitHF3zlllll9llllxVllll5@@@@@@@@@@; ABTEST=5|1572589248|v1; weixinIndexVisited=1; PHPSESSID=r3cieq73otgi5os6l4q1kedrj5; SNUID=15B6A80E7C78EB38EA9007D57DD5864B; successCount=1|Fri, 01 Nov 2019 08:22:14 GMT; sct=1; JSESSIONID=aaaY08IhgrOl1_y54Yw4w; ppinf=5|1572596274|1573805874|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo2OlNoYWxvcnxjcnQ6MTA6MTU3MjU5NjI3NHxyZWZuaWNrOjY6U2hhbG9yfHVzZXJpZDo0NDpvOXQybHVFclpESW1Qb1Q0LTQ1VEFqQnhfdzRrQHdlaXhpbi5zb2h1LmNvbXw; pprdig=KtmFAO5teojm9VCilZlXXRlp-V9vxFwM4a9hAFh6vHAqLZLFTcJwZcwpp8NAnWQewu2lSWZC7rHLbe6ivlWztnI370klDDVKNJrQ9cDxhdrqnWAj2UzSg9WmWJGhNZh6qLu9D1B-q94lnXhb23LcH_ZDXSjV4Rj0Yi3nKrwQIbw; sgid=03-35189841-AV276jInqC9vDYkK4IUXUEM; ppmdig=1572596274000000e1695be13c3c78aaffd96fab12435e72',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

keyword = '风景'
proxy_pool_url = 'http://127.0.0.1:5555/random'

proxy = None
max_count = 5

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    print('Crawling',url)
    print('Trying Count',count)
    global proxy
    if count>=max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http':'http://' + proxy
            }
            response = requests.get(url,allow_redirects=False,headers=headers,proxies=proxies)
        else:
            # allow_redirects=False这个参数意思让其不要自动的处理跳转
            response = requests.get(url,allow_redirects=False,headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # IP被封了
            proxy = get_proxy()
            if proxy:
                print("Using proxy",proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred',e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)




def get_index(keyword,page):
    data = {
        'query':keyword,
        'type':2,
        'page':page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items  = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield 'https://weixin.sogou.com'+item.attr('href')

def main():
    for page in range(1,3):
        html = get_index(keyword,page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                print(article_url)

if __name__ == "__main__":
    main()