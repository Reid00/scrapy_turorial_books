# -*- coding: utf-8 -*-
import os
import scrapy
import pandas as pd
from ..items import BooksItem
from scrapy.linkextractors import LinkExtractor  # 解析页面中的链接


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books_info = response.xpath('//ol[@class="row"]')
        book_links = books_info.xpath('//h3/a/@href').extract()

        for book_link in book_links:
            book_link = response.urljoin(book_link)
            yield scrapy.Request(book_link, callback=self.parse_book)

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        # book_le = LinkExtractor(restrict_css='article.product_pod h3 a')
        # book_links = book_le.extract_links(response)
        # for book_link in book_links:
        #     yield scrapy.Request(book_link.url, callback=self.parse_book)  # 详情页Request，调用self.parse_book方法解析
        #
        # next_le = LinkExtractor(restrict_css='ul.pager li.next a')
        # next_link = next_le.extract_links(response)
        # if next_link:
        #     yield scrapy.Request(next_link[0].url, callback=self.parse)  # 下一列表页Request，调用自身方法解析

    def parse_book(self, response):
        item = BooksItem()
        info = response.xpath('//article[@class="product_page"]')
        item['name'] = info.xpath('//h1/text()').extract_first().strip()
        item['price'] = info.xpath('//p[@class="price_color"]/text()').extract_first().strip()
        item['rating'] = info.xpath('//p[starts-with(@class,"star-rating")]').re_first(
            r'star-rating(?P<rating>([^"]+))').strip()
        item['review'] = response.xpath(
            '//table[@class="table table-striped"]/tr[last()]/td/text()').extract_first().strip()
        item['stock'] = response.xpath(
            '//table[@class="table table-striped"]/tr[last()-1]/td/text()').extract_first().strip()
        item['upc'] = response.xpath('//table[@class="table table-striped"]/tr[1]/td/text()').extract_first().strip()

        yield item
