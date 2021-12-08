import hashlib
import uuid

import requests
from fake_useragent import UserAgent
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.utils.python import to_bytes

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get?type=http").json()


class ImgsPipeline(object):
    def process_item(self, item, spider):
        return item


class ImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            ua = UserAgent()
            self.default_headers['User-Agent'] = ua.random
            req = Request(image_url, headers=self.default_headers)
            proxy_str = "http://{0}".format(get_proxy()['proxy'])
            print(proxy_str)
            req.meta["proxy"] = proxy_str
            yield req

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + uuid.uuid4().hex
        return f'full/{image_guid}.jpg'