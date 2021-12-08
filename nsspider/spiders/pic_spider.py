import logging
import re
import uuid

import requests as requests
import scrapy
from scrapy_splash import SplashRequest
from faker import Faker
from nsspider.items import ImgsItem

logging.getLogger('faker').setLevel(logging.ERROR)
BASEURL = "https://szszet.one"
BASEURL_WITH_SLASH = "https://szszet.one/"
# https://ip.jiangxianli.com/api/proxy_ip
def get_proxy():
    r = requests.get(
        "https://dps.kdlapi.com/api/getdps/?orderid=903897512304377&num=1&pt=1&format=json&sep=1")
    proxy_str = r.json()['data']['proxy_list'][0]
    return proxy_str



class PicSpider(scrapy.Spider):
    name = 'pic-spider'

    def start_requests(self):
        urls = []
        with open("./resource/url.txt", "r") as f:
            for line in f.readlines():
                urls.append(line.strip('\n'))
        print(urls)
        # urls = ["http://icanhazip.com"]
        # timeout 时间随网络情况而定30 20 10
        for url in urls:
            yield SplashRequest(args={'images': 1, 'timeout': 50, 'wait': 20}, url=url, callback=self.pic_parse,
                                dont_filter=True)

    def pic_parse(self, response):
        print('---------collect picture from each url------------')
        print(response.url)
        result_list = response.css('img::attr(src)').getall()
        pics_suffix = []
        for result in result_list:
            if len(result) < 100 and not re.match('(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|jpeg)', result):
                pics_suffix.append(result)
        img_urls = list(map(lambda x: BASEURL + x, pics_suffix))
        print(img_urls)


        # if img_urls:
        #     item = ImgsItem()
        #     item['image_urls'] = img_urls
        #     yield item


        #download the pictures
        file_path = './pic/'
        for img_url in img_urls:
            file_name = uuid.uuid4().hex
            full_picture_name = file_path + file_name + ".jpg"
            # print(file_path + file_name + ".jpg")
            download(full_picture_name, img_url)


def download(file_path, picture_url):
    username = "mz2986"
    password = "61n2986u"
    # fake header
    fake = Faker()
    headers = {'User-Agent': fake.user_agent()}
    retry_count = 5
    while retry_count > 0:
        try:
            proxy_ip = get_proxy()
            print(picture_url + " - " + proxy_ip + " - " + file_path)
            proxies = {
                "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
                "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
            }
            r = requests.get(picture_url, headers=headers, proxies=proxies) # , verify=False
            with open(file_path, 'wb') as f:
                f.write(r.content)
            return
        except Exception:
            retry_count -= 1
            if retry_count == 0:
                print("failed")
    return None


