import re
import uuid
from time import sleep
import requests as requests
import scrapy
from scrapy_splash import SplashRequest
from faker import Faker
from nsspider.items import PicItem

BASEURL = "https://szszet.com"
BASEURL_WITH_SLASH = "https://szszet.com/"


class UrlSpider(scrapy.Spider):
    name = 'pic-spider'

    def start_requests(self):
        urls = []
        with open("./resource/url.txt", "r") as f:
            for line in f.readlines():
                urls.append(line.strip('\n'))
        print(urls)
        for url in urls:
            yield SplashRequest(args={'images': 1, 'timeout': 20, 'wait': 20}, url=url, callback=self.pic_parse,
                                dont_filter=True)

    def pic_parse(self, response):
        print('---------collect picture from each url------------')
        print(response.url)
        pics_suffix = response.css('img::attr(src)').getall()
        pics_suffix = list(filter(lambda x: len(x) < 100, pics_suffix))
        img_urls = list(map(lambda x: BASEURL + x, pics_suffix))
        print(img_urls)

        # download the pictures
        file_path = './pic/'
        for img_url in img_urls:
            file_name = uuid.uuid4().hex
            full_picture_name = file_path + file_name + ".jpg"
            # print(file_path + file_name + ".jpg")
            download(full_picture_name, img_url)


def download(file_path, picture_url):
    # fake header
    fake = Faker()
    headers = {'User-Agent': fake.user_agent()}
    # print(headers)

    try:
        r = requests.get(picture_url, headers=headers)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    except:
        print("ERROR")