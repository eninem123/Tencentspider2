# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

from deeptencent.items import DeeptencentItem,PositionItem


class DtencentSpider(CrawlSpider):
    name = 'dtencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=10']
    rules = [
        Rule(LinkExtractor(allow=r"position\.php\?&start=\d+"),callback="parse_page", follow=True),
        Rule(LinkExtractor(allow=r"position_detail\.php\?id=\d+"),callback="parse_position", follow=False)
    ]

    def parse_page(self, response):
        # 提取当前页面中所有职位的结点列表
        node_list = response.xpath("//tr[@class='odd'] | //tr[@class='even']")

        # 迭代每个结点，并提取职位数据
        for node in node_list:
            item = DeeptencentItem()

            item["position_name"] = node.xpath("./td[1]/a/text()").extract_first()
            item["position_link"] = "https://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item["position_type"] = node.xpath("./td[2]/text()").extract_first()
            item["people_number"] = node.xpath("./td[3]/text()").extract_first()
            item["work_location"] = node.xpath("./td[4]/text()").extract_first()
            item["publish_times"] = node.xpath("./td[5]/text()").extract_first()

            yield item

    # 处理职位详情页（处理每个职位的2条信息）
    def parse_position(self, response):
        item = PositionItem()

        item['position_zhize'] = "\n".join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item['position_yaoqiu'] = "\n".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item