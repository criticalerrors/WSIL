from django.db import models
from django.utils import timezone
import datetime
import requests
import threading


def tomorrow():
    return timezone.now() + datetime.timedelta(days=1)

# Create your models here.

class RepositoryUsingIt(models.Model):
    language = models.CharField(unique=True, max_length=30)
    repository_count = models.IntegerField()

    @classmethod
    def create(cls, language_name, language_count):
        rui = cls(language=language_name, repository_count=language_count)
        return rui


class QuestionOnIt(models.Model):
    tag = models.CharField(unique=True, max_length=30)
    count = models.IntegerField()
    cache_date = models.DateTimeField(null=True, default=tomorrow)

    @classmethod
    def get_count_for_lang(cls, lang):
        in_db = cls.objects.filter(tag__iexact=lang)
        t = None
        if len(in_db) == 1:
            in_db = in_db[0]
            if in_db.cache_date > timezone.now():
                print("Cached!")
                return in_db
            else:
                t = threading.Thread(target=clear_cache, args=(QuestionOnIt,))
                t.start()
        url = "https://api.stackexchange.com/2.2/tags?order=desc&sort=popular&inname="+lang+"&site=stackoverflow"
        json = {}
        try:
            r = requests.get(url)
            json = r.json()['items']
        except ConnectionError as ex:
            print(ex)
        except Exception as ex:
            print(ex)
        for tag in json:
            if lang.lower() == tag['name'].lower():
                try:
                    tc = cls(tag=tag['name'], count=tag['count'])
                    if t:
                        t.join()
                    tc.save()
                    return tc
                except Exception as ex:
                    print(ex)


class Language(models.Model):
    name = models.CharField(unique=True, max_length=30)


class LibraryOrFramework(models.Model):
    name = models.CharField(unique=True, max_length=40)
    type = models.CharField(max_length=30, null=True)
    initial_release = models.CharField(max_length=100, null=True)
    stable_release = models.CharField(max_length=100, null=True)
    repository = models.URLField(null=True)
    development_status = models.CharField(max_length=10, null=True)
    language = models.ManyToManyField(Language, null=True)
    license = models.CharField(max_length=10, null=True)
    website = models.URLField(null=True)
    description = models.CharField(null=True, max_length=300)


class Features(models.Model):
    library_framework_name = models.CharField(unique=True, max_length=40)
    ajax = models.CharField(max_length=30, null=True)
    mvc_framework = models.CharField(max_length=40, null=True)
    mvc_push_pull = models.CharField(max_length=40, null=True)
    localization = models.CharField(max_length=40, null=True)
    orm =  models.CharField(max_length=40, null=True)
    testing_framework =  models.CharField(max_length=40, null=True)
    db_migration_framework = models.CharField(max_length=40, null=True)
    security_framework = models.CharField(max_length=40, null=True)
    template_framework = models.CharField(max_length=40, null=True)
    caching_framework = models.CharField(max_length=40, null=True)
    form_validation_framework = models.CharField(max_length=40, null=True)


class InterestOverTimeLanguage(models.Model):
    language_name = models.CharField(max_length=30)
    date = models.DateTimeField(null=True)
    interest_rate = models.IntegerField(null=True)

    class Meta:
        unique_together = (("language_name", "date"),)


class InterestOverTimeFrameworkLibrary(models.Model):
    fw_or_lib = models.CharField(max_length=30)
    date = models.DateTimeField(null=True)
    interest_rate = models.IntegerField(null=True)

    class Meta:
        unique_together = (("fw_or_lib", "date"),)


class InterestByRegionLanguage(models.Model):
    language = models.CharField(max_length=30)
    region = models.CharField(max_length=30, null=True)
    interest_rate = models.IntegerField(null=True)

    class Meta:
        unique_together = (("language", "region"),)


class InterestByRegionFrameworkLibrary(models.Model):
    fw_or_lib = models.CharField(max_length=30)
    region = models.CharField(max_length=30, null=True)
    interest_rate = models.IntegerField(null=True)

    class Meta:
        unique_together = (("fw_or_lib", "region"),)


class Course(models.Model):
    course_id = models.CharField(unique=True, max_length=30)
    slug =  models.CharField(max_length=30, null=True)
    course_type =  models.CharField(max_length=30, null=True)
    logo = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    description = models.CharField(max_length=150, null=True)
    workload = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)
    cache_date = models.DateTimeField(null=True, default=tomorrow)


class CoursePartner(models.Model):
    partner_id = models.CharField(max_length=30, unique= True)
    course_id = models.ManyToManyField(Course, null=True)
    partner_name = models.CharField(max_length=30, null=True)
    partner_image = models.URLField(null=True)
    cache_date = models.DateTimeField(null=True, default=tomorrow)


class Job(models.Model):
    job_title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150, null=True)
    post_date = models.CharField(max_length=10, null=True)
    company_name = models.CharField(max_length=30, null=True)
    company_url = models.URLField(null=True)
    location_name = models.CharField(max_length=30, null=True)
    lat = models.CharField(max_length=30, null=True)
    query = models.CharField(max_length=30, null=True)
    cache_date = models.DateTimeField(null=True, default=tomorrow)

    @classmethod
    def get_all_job_for(cls, keyword):
        url = "http://api.indeed.com/ads/apisearch?publisher=6284576268691023&v=2&format=json&q=" + keyword
        Job.objects.filter(query__contains=keyword)


def clear_cache(model):
    print("Lazy delete")
    model.objects.filter(cache_date__lt=timezone.now()).delete()