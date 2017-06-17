# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# We need to access directly to the Django's model in order to manipulate
# the many to many relations
from wsil.models import LibraryOrFramework, Language
from django.core.exceptions import ObjectDoesNotExist

class WikiscraperPipeline(object):
    def process_item(self, item, spider):
        fw_lib_obj = item['item']
        for key in fw_lib_obj.keys(): # All elements are lists with only one element.
            fw_lib_obj[key] = fw_lib_obj[key][0] # We extract the single element to remove the list

        row = LibraryOrFramework(**fw_lib_obj) # All the fields addend by the scraper are extracted
        row.save()

        languages = item['language']
        for lang in languages:
            lang_to_add = None
            try:
                lang_to_add = Language.objects.get(name=lang)
            except ObjectDoesNotExist as ex: # The language does not exist in the db
                lang_to_add = Language(name=lang) # So we add it ourselves
                lang_to_add.save()
            finally:
                row.language.add(lang_to_add)

        return item;