import scrapy

from wikiscraper.items import FeaturesItem, LibraryOrFrameworkItem

class LibraryOrFrameworkSpider(scrapy.Spider):
    name = "library_or_framework"
    start_urls = [
        'https://en.wikipedia.org/wiki/Comparison_of_web_frameworks'
    ]

    def parse(self, response):
        for xx in enumerate(response.xpath("")):
            yield xx
