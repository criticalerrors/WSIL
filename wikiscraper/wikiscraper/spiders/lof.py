import scrapy

from wikiscraper.items import FeaturesItem, LibraryOrFrameworkItem
from scrapy.http import Request
from scrapy.loader import ItemLoader

class LibraryOrFrameworkSpider(scrapy.Spider):
    name = "library_or_framework"
    start_urls = [
        'https://en.wikipedia.org/wiki/Comparison_of_web_frameworks'
    ]


    def parse(self, response):
        last_request = None
        #language = elem.xpath('//*[@id="mw-content-text"]/div/h3[position()<15]/span/text()').extract()

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
            stable_version = cells[-2].xpath('./text()').extract_first()
            release_date = cells[-3].xpath('./text()').extract_first()

            # Getting the url of the detailed page
            fw_lib_url = 'https://en.wikipedia.org' + elem.xpath('./th/a/@href').extract_first()
            self.log('Sending request to ' + fw_lib_url)
            request = Request(fw_lib_url, callback=self.get_details)

            request.meta['name'] = name
            if language[0] != "Others":
                request.meta['language'] = language
            request.meta['stable_version'] = stable_version
            request.meta['rel_date'] = release_date
            request.meta['license'] = lic

            yield request


    def get_details(self, response):
        self.log('Starting the second parsing phase')
        loader = ItemLoader(item=LibraryOrFrameworkItem(), response=response)

        loader.add_value('name', response.meta['name'])

        if 'language' is response.meta:
            loader.add_value('language', response.meta['language'])
        loader.add_value('stable_release', response.meta['stable_version'])
        # Waiting for the update of FrameworkOrLibrary model
        loader.add_value('release_date', response.meta['rel_date'])
        loader.add_xpath('description', '//*[@id="mw-content-text"]/div/p[1] | //*[@id="mw-content-text"]/p[1]')

        license_found = False
        for row in response\
                    .xpath('//*[@id="mw-content-text"]/div/table[position()<=3]/tr'):
            header = row.xpath('./th/a/text() | ./th/text()').extract_first()
            key, value = self.get_key_value(header, row)
            if key:
                if key == 'license':
                    license_found = True
                loader.add_value(key, value)
        # If it not found the license in the main page
        # it will use the license found in the start page
        if not license_found:
            loader.add_value('license', response.meta['license'])

        return loader.load_item()


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
            value = elem.xpath('./td/a/text() | ./td/text()').extract_first()
            plain_text = elem.xpath('./td/text()').extract_first()
            value = value + plain_text if plain_text else value
            return ('license', value)
        elif key == 'Website':
            return ('website', elem.xpath('./td/span/a/@href').extract_first())
        else:
            return (None, None)
