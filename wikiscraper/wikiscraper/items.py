# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from wsil.models import Features, LibraryOrFramework


class WikiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LibraryOrFrameworkItem(DjangoItem):
    django_model = LibraryOrFramework


class FeaturesItem(DjangoItem):
    django_model = Features

