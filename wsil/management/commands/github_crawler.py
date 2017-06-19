import gzip
from urllib import request
import json
import threading
import logging
logger = logging.getLogger(__name__)

from wsil.models import RepositoryUsingIt

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

allowed_types = ['CreateEvent']
count_dict = dict()
file = 'wsil/management/commands/last-date.txt'


class Command(BaseCommand):
    help = "Populate db from GitHub repositories"

    def _create_language_stats(self):
        start()

    def handle(self, *args, **options):
        self._create_language_stats()


def start():
    first_y, first_m, first_d, first_h = 0,0,0,0
    last_y, last_m, last_d, last_h = 0,0,0,0

    with open(file) as f:
        line = f.readline()
        first_y, first_m, first_d, first_h = line.split("-")

    for y in range(int(first_y), 2017):
        for m in range(int(first_m), 13):
            for d in range(int(first_d), 32):
                for h in range(int(first_h), 24):
                    yy = str(y)
                    mm = str(m) if m >= 10 else "0" + str(m)
                    dd = str(d) if d >= 10 else "0" + str(d)
                    hh = str(h)
                    url = "http://data.githubarchive.org/{}-{}-{}-{}.json.gz".format(yy, mm, dd, hh)
                    print(url)
                    try:
                        request.urlretrieve(url, "file.gz")
                    except Exception as ex:
                        print(ex)
                    last_y, last_m, last_d, last_h = yy, mm, dd, hh
                    try:
                        analyze_file("file.gz")
                    except Exception as ex:
                        print(ex)
                        continue
                    first_m = 1
                    first_d = 1
                    first_h = 0
                word = last_y + "-" + last_m + "-" + last_d + "-" + last_h
                save_into_file(word)
                save_into_db()


def analyze_file(wfile):
    with gzip.open(wfile, 'r') as f:
        for row in [x.decode('utf8').strip() for x in f.readlines()]:
            obj = json.loads(row)
            if 'repository' not in obj.keys():
                continue
            if 'language' not in obj['repository'].keys():
                continue
            if obj['repository'] is None or obj['repository']['language'] is None:
                continue
            language = obj['repository']['language']
            if language in count_dict:
                count_dict[language] += 1
            else:
                count_dict[language] = 1


def save_into_file(word):
    with open(file, 'w') as f:
        f.write(word)


def save_into_db():
    for language in count_dict:
        if language is None:
            print("NONE")
            continue
        try:
            language_instance = RepositoryUsingIt.objects.get(language=language)
            language_instance.repository_count = count_dict[language]
            language_instance.save()
        except ObjectDoesNotExist as odne:
            try:
                language_instance = RepositoryUsingIt.create(language_name=language, language_count=count_dict[language])
                language_instance.save()
            except Exception as ex:
                print(language)
                print(ex)
    logger.info("Data saved into db")

