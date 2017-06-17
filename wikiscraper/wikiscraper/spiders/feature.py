import scrapy

from html import unescape
from .utils import cleanhtml, removesquares
from scrapy.loader import ItemLoader
from wikiscraper.items import FeaturesItem
from django.db.utils import IntegrityError

class FeatureSpider(scrapy.Spider):
    name = "features"
    start_urls = [
        'https://en.wikipedia.org/wiki/Comparison_of_web_frameworks'
    ]

    # Character used to indicate that the value is missing
    empty_field_placeholder = [
        '_', '-', '?', 'N/A'
    ]

    def __init__(self, *args, **kwargs):
        # For each table, it contain for each attribute the associated position
        self.column_position = {
            'library_framework_name': 0,
            'ajax': 0,
            'mvc_framework': 0,
            'mvc_push_pull': 0,
            'localization': 0,
            'orm': 0,
            'testing_framework': 0,
            'db_migration_framework': 0,
            'security_framework': 0,
            'template_framework': 0,
            'caching_framework': 0,
            'form_validation_framework': 0,
        }
        super(FeatureSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        for table in response.xpath('//*[@id="mw-content-text"]/div/table[position() >= 18]'):
            # Update column positions
            self.update_positions(table.xpath('./tr[1]'))
            for elem in table.xpath('./tr[position()>1]'):

                if elem.xpath('count(./td)').extract_first() == '0.0': # We have found another header
                    continue # We will skip it

                cells = list(elem.xpath('./*').extract())

                feature = FeaturesItem()
                for col in self.column_position:
                    position = self.column_position[col]
                    if position >= len(cells): # Missing cell to the end
                        break
                    parsed_value = unescape(removesquares(cleanhtml(cells[position])))
                    # It verify that the value is not missing
                    if not len(parsed_value) == 0 and not parsed_value in self.empty_field_placeholder:
                        feature[col] = parsed_value

                try:
                    feature.save()
                    self.log("Saved {}".format(feature))
                except IntegrityError as ex:
                    # There are two rows with name 'Fusebox'. The second is missing in the framework list.
                    # So we will not add it to the db
                    self.log("IntegrityError: {}".format(ex))
                    self.log("Caused by item: {}".format(feature))

    # For each table, check the correct positions where the parser can find the needed values
    # Not all the tables have the same dimension!!!
    def update_positions(self, col_header):
        for index, col_name in enumerate(col_header.xpath('./th').extract()):
            parsed_col_name = cleanhtml(col_name)
            if parsed_col_name == "Project":
                self.column_position['library_framework_name'] = index
            elif parsed_col_name == "Ajax":
                self.column_position['ajax'] = index
            elif parsed_col_name == "MVC framework":
                self.column_position['mvc_framework'] = index
            elif parsed_col_name == "MVC push-pull":
                self.column_position['mvc_push_pull'] = index
            elif parsed_col_name == "i18n &amp; L10n?":
                self.column_position['localization'] = index
            elif parsed_col_name == "ORM":
                self.column_position['orm'] = index
            elif parsed_col_name == "Testing framework(s)":
                self.column_position['testing_framework'] = index
            elif parsed_col_name == "DB migration framework(s)":
                self.column_position['db_migration_framework'] = index
            elif parsed_col_name == "Security framework(s)":
                self.column_position['security_framework'] = index
            elif parsed_col_name == "Template framework(s)":
                self.column_position['template_framework'] = index
            elif parsed_col_name == "Caching framework(s)":
                self.column_position['caching_framework'] = index
            elif parsed_col_name == "Form validation framework(s)":
                self.column_position['form_validation_framework'] = index

    # Reset the positions saved in the column_position attribute
    def reset_column_index(self):
        for col in self.column_position:
            self.column_position[col] = 0