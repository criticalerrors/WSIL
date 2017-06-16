# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class WikiscraperPipeline(object):
    def process_item(self, item, spider):
        item['description'][0] = self.cleanhtml(item['description'][0])
        for key in item.keys(): # All elements are lists of only one element.
            item[key] = item[key][0] # We extract the element to remove the list

        item.save()
        return item;


    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext