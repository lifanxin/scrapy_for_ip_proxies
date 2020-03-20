# -*- coding: utf-8 -*-
import time
import scrapy
from ..items import IpProxiesItem


class A66ipSpider(scrapy.Spider):
    name = '66ip'
    allowed_domains = ['66ip.cn']
    start_urls = ['http://www.66ip.cn/index.html']

    def parse(self, response):
        ip_list = response.xpath('//div[@id="main"]//table//tr[position()>1]')
        for ip_info in ip_list:
            ip_proxy = IpProxiesItem()
            ip_proxy['ip'] = ip_info.xpath('./td[1]/text()').extract_first()
            ip_proxy['port'] = ip_info.xpath('./td[2]/text()').extract_first()
            ip_proxy['address'] = ip_info.xpath(
                './td[3]/text()').extract_first()

            yield ip_proxy

        next_url = response.xpath('//a[text()="»"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            time.sleep(2)
            print('new_page {}'.format(next_url))

            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )
