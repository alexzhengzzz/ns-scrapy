import re
import scrapy
from scrapy_splash import SplashRequest

BASEURL = "https://www.szszet.one"
BASEURL_WITH_SLASH = "https://www.szszet.one/"


class UrlSpider(scrapy.Spider):
    name = 'url-spider'

    def start_requests(self):
        start_urls = ['https://www.szszet.com/#/index', ]
        # deal with the front-end render
        for url in start_urls:
            yield SplashRequest(url=url, callback=self.url_parse)

    # extract all the route of the website
    def url_parse(self, response):
        print("-----------------start scraping-------------------")
        print("-----------------collecting all the urls -------------------")
        hrefs = response.css("a::attr(href)").getall()
        page_suffix_list = list(set(list(filter(lambda x: re.match('#/*', x) is not None, hrefs))))
        urls = list(map(lambda x: BASEURL_WITH_SLASH + x, page_suffix_list))
        with open('./resource/url.txt', 'w') as f:
            f.write('\n'.join(urls))
