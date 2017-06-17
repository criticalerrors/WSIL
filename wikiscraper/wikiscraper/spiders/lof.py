import scrapy
import re

from wikiscraper.items import FeaturesItem, LibraryOrFrameworkItem
from scrapy.http import Request
from scrapy.loader import ItemLoader
from .utils import cleanhtml

class LibraryOrFrameworkSpider(scrapy.Spider):
    name = "library_or_framework"
    start_urls = [
        'https://en.wikipedia.org/wiki/Comparison_of_web_frameworks'
    ]


    def parse(self, response):
        for elem in response\
                        .xpath('//*[@id="mw-content-text"]/div/table[position()<18 and position()>2]/tr[position()>1]'):
            # Framework or library name extraction
            language = elem.xpath('./../preceding-sibling::h3[1]/span/text()').extract() # Get the title right before the table
            name = elem.xpath('./th/a/text()').extract_first()
            acronym = elem.xpath('./th/text()').extract_first()
            if acronym: # There may be an acronym next to the name
                name += acronym

            self.log("Next element: " + name)
            # Get version and release
            cells = list(elem.xpath('./td')) # In some table there is also a column named 'Language'
            # We start from the last column and we go backward
            lic = cells[-1].xpath('./text() | ./a/text()').extract_first()
            release_date = cells[-2].xpath('./text()').extract_first()
            stable_version = cells[-3].xpath('./text()').extract_first()

            # Getting the url of the detailed page
            base_path = elem.xpath('./th/a/@href').extract_first()
            if 'http' in base_path: # Some entries have a link to their homepage. We will exclude it
                continue
            fw_lib_url = 'https://en.wikipedia.org' + base_path
            self.log('Sending request to ' + fw_lib_url)
            request = Request(fw_lib_url, callback=self.get_details)


            request.meta['name'] = name
            if language[0] != "Others":
                request.meta['language'] = language
            else:
                # On the table named Others, there are a column with the frameworks' languages
                lang = cells[-4].xpath('.').extract_first()
                request.meta['language'] = [l.lstrip() for l in cleanhtml(lang).split(',')]

            request.meta['stable_version'] = stable_version
            request.meta['rel_date'] = release_date
            request.meta['license'] = lic

            yield request


    # Continue the parsing in the framework/library main page
    def get_details(self, response):
        self.log('Starting the second parsing phase')
        loader = ItemLoader(item=LibraryOrFrameworkItem(), response=response)

        # Load the values obtained in the first phase
        loader.add_value('name', response.meta['name'])

        language = response.meta['language']

        loader.add_value('stable_release', response.meta['stable_version'])
        loader.add_value('release_date', response.meta['rel_date'])


        descr = response.xpath('//*[@id="mw-content-text"]/div/p[1] | //*[@id="mw-content-text"]/p[1]').extract_first()
        cleaned_descr = cleanhtml(descr)
        loader.add_value('description', cleaned_descr)

        license_found = False
        for row in response\
                    .xpath('//*[@id="mw-content-text"]/div/table[position()<=3]/tr'):
            header = row.xpath('./th/a/text() | ./th/text()').extract_first()
            key, value = self.get_key_value(header, row)
            if key:
                if key == 'license': # If we find the license in the main page, we will use it
                    license_found = True
                loader.add_value(key, value)
        # If we not found the license in the main page
        # We will use the license found on the start page
        if not license_found:
            loader.add_value('license', response.meta['license'])

        return {
            "item": loader.load_item(),
            "language": language
            # We need to return the language separately in order to manage the many to many relation
        }

    # Given a couple (key, elem), obtained during the scraping, he returns the valid couple (key1, value1)
    # to add to the db. If key is not valid, he will return the tuple (None, None)
    @staticmethod
    def get_key_value(key, elem):
        if key == 'Initial release':
            return ('initial_release', elem.xpath('./td/text()').extract_first())
        elif key == 'Repository':
            return ('repository', elem.xpath('./td/span/a/@href').extract_first())
        elif key == 'Development status':
            return ('development_status', elem.xpath('./td/text()').extract_first())
        elif key == 'Type':
            return ('type', elem.xpath('./td/a/text()').extract_first())
        elif key == 'License': #There may be a combination of link and plain text
            value = elem.xpath('./td').extract_first()
            parsed_value = re.sub(r'\[.*?\]', ' ', cleanhtml(value))
            return ('license', parsed_value)
        elif key == 'Website':
            urls = [url for url in elem.xpath('./td//a/@href').extract()]
            return ('website', ','.join(urls))
        else:
            return (None, None)