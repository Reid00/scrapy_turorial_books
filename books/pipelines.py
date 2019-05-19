# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os


class BooksPipeline(object):
    rating_map = {

        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def process_item(self, item, spider):
        origin_rating = item.get('rating')
        if origin_rating:
            item['rating'] = self.rating_map[origin_rating]
        df = pd.DataFrame({
            'book name': [item['name']],
            'book upc': [item['upc']],
            'book price': [item['price']],
            'book stock': [item['stock']],
            'book rating': [item['rating']],
            'book review': [item['review']],
        })

        if not os.path.exists('book.csv'):
            df.to_csv('book.csv', index=None, header=True, mode='a')
        else:
            df.to_csv('book.csv', index=None, header=None, mode='a')
