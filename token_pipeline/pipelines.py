# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# 导入项目设置
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from os.path import join, splitext
import six
from PIL import Image
from scrapy.utils.misc import md5sum
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
class TokenPipelinePipeline(object):
    def process_item(self, item, spider):
        return item

class TokenFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'], meta={'proxy': 'http://127.0.0.1:1087', 'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename, file_extension = splitext(item['url'])
        return item['name'] + file_extension

class CoinImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'], meta={'proxy': 'http://127.0.0.1:1087', 'item': item})
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename, file_extension = splitext(item['url'])
        return item['name'] + file_extension

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height})
        return checksum
        
    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.MIN_WIDTH, self.MIN_HEIGHT))

        yield path, orig_image, BytesIO(response.body)

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf
