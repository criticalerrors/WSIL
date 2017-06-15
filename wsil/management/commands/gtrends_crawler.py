from wsil import models
from pytrends.request import TrendReq
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Populate Google Trends data"

    def _create_trends_stats(self):
        start()

    def handle(self, *args, **options):
        self._create_trends_stats()


def start():
    GOOGLE_USR = ""
    GOOGLE_PWD = ""
    treq = None
    try:
        GOOGLE_USR = os.environ['GOOGLE_ACCOUNT']
        GOOGLE_PWD = os.environ['GOOGLE_PASSWORD']
    except Exception as ex:
        print("GOOGLE_ACCOUNT and GOOGLE_PASSWORD not set. " + ex)

    try:
        treq = TrendReq(GOOGLE_USR, GOOGLE_PWD)
    except Exception as ex:
        print("Username or password not valid. " + ex)
    print("Connected")

    #LANGUAGES
    all_languages = [i.name for i in models.Language.objects.all()]
    languages_cnt = len(all_languages)
    for i in range(0, languages_cnt+1, 5):
        print("Fetch for " + ", ".join(all_languages[i:i+4]))
        treq.build_payload(kw_list=all_languages[i:i+4])
        populate_iot(treq.interest_over_time())
        populate_ior(treq.interest_by_region())
    if languages_cnt % 5 != 0:
        slice_index = languages_cnt - int(languages_cnt / 5) * 5
        print("Fetch for " + ", ".join(all_languages[-slice_index]))
        treq.build_payload(kw_list=all_languages[-slice_index])
        populate_iot(treq.interest_over_time())
        populate_ior(treq.interest_by_region())
    print("Interest over time language completed.")

    #FRAMEWORKS
    print("Interest over time framework started.")
    all_fw = [i.name for i in models.LibraryOrFramework.objects.all()]
    fw_cnt = len(all_fw)
    for i in range(0, fw_cnt + 1, 5):
        print("Fetch for " + ", ".join(all_languages[i:i+4]))
        treq.build_payload(kw_list=all_languages[i:i+4])
        populate_iot_fw(treq.interest_over_time())
        populate_ior_fw(treq.interest_by_region())
    if fw_cnt % 5 != 0:
        slice_index = fw_cnt - int(fw_cnt / 5) * 5
        print("Fetch for " + ", ".join(all_fw[-slice_index]))
        treq.build_payload(kw_list=all_languages[-slice_index])
        populate_iot_fw(treq.interest_over_time())
        populate_ior_fw(treq.interest_by_region())
    print("Interest over time framework completed.")


def populate_iot(dataframe):
    indices_row = [i for i in dataframe.index]
    indices_col = [str(i) for i in dataframe.columns]
    objs = []
    for i in indices_col:
        for j in range(0, len(dataframe[i])):
            objs.append(models.InterestOverTimeLanguage(language_name=i, date=indices_row[j],
                                                        interest_rate=dataframe[i][j]))
        models.InterestOverTimeLanguage.objects.bulk_create(objs)
        print("Data for {} inserted".format(i))
        objs = []


def populate_ior(dataframe):
    indices_row = [str(i) for i in dataframe.index] # get regions
    indices_col = [str(i) for i in dataframe.columns]
    objs = []
    for i in indices_col:
        for j in range(0, len(dataframe[i])):
            objs.append(models.InterestByRegionLanguage(language=i, region=indices_row[j],
                                                        interest_rate=dataframe[i][j]))
        models.InterestByRegionLanguage.objects.bulk_create(objs)
        print("Data by region for {} inserted".format(i))
        objs = []


def populate_iot_fw(dataframe):
    indices_row = [i for i in dataframe.index]
    indices_col = [str(i) for i in dataframe.columns]
    objs = []
    for i in indices_col:
        for j in range(0, len(dataframe[i])):
            objs.append(models.InterestOverTimeFrameworkLibrary(fw_or_lib=i, date=indices_row[j],
                                                        interest_rate=dataframe[i][j]))
        models.InterestOverTimeFrameworkLibrary.objects.bulk_create(objs)
        print("Data for {} inserted".format(i))
        objs = []


def populate_ior_fw(dataframe):
    indices_row = [str(i) for i in dataframe.index] # get regions
    indices_col = [str(i) for i in dataframe.columns]
    objs = []
    for i in indices_col:
        for j in range(0, len(dataframe[i])):
            objs.append(models.InterestByRegionFrameworkLibrary(fw_or_lib=i, region=indices_row[j],
                                                        interest_rate=dataframe[i][j]))
        models.InterestByRegionFrameworkLibrary.objects.bulk_create(objs)
        print("Data by region for {} inserted".format(i))
        objs = []
