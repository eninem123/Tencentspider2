# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import json

from deeptencent.items import DeeptencentItem, PositionItem


class DeeptencentPipeline(object):

    # 爬虫启动时执行一次
    def open_spider(self, spider):
        self.f = open("tencent.json", "w")

    # 必须实现的，用来处理每一个item数据
    def process_item(self, item, spider):
        if isinstance(item, DeeptencentItem):
            content = json.dumps(dict(item)) + ",\n"
            self.f.write(content)

        return item

    # 爬虫关闭时执行一次
    def close_spider(self, spider):
        self.f.close()



class PositionJsonPipeline(object):

    # 爬虫启动时执行一次
    def open_spider(self, spider):
        self.f = open("position.json", "w")

    # 必须实现的，用来处理每一个item数据
    def process_item(self, item, spider):
        if isinstance(item, PositionItem):
            content = json.dumps(dict(item)) + ",\n"
            self.f.write(content)

        return item

    # 爬虫关闭时执行一次
    def close_spider(self, spider):
        self.f.close()