from django.db import models

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



"""InterestOverTimeLanguage(?language_name, ?date, ?interest_rate)"""

class InterestOverTimeLanguage(models.Model):
    language_name = models.CharField(unique= True, max_length=30)
    date = models.CharField(max_length=20, null=True)
    interest_rate = models.CharField(max_length=10, null=True)



"""InterestOverTimeFrameworkLibrary(?fw_or_lib, ?date, ?interest_rate)"""
class InterestOverTimeFrameworkLibrary(models.Model):
    fw_or_lib = models.CharField(unique=True, max_length=30)
    date = models.CharField(max_length=20, null=True)
    interest_rate = models.CharField(max_length=10, null=True)

""" InterestByRegionLanguage(?language, ?region, ?interest_rate)"""
class InterestByRegionLanguage(models.Model):
    language = models.CharField(unique=True, max_length=30)
    region = models.CharField(max_length=30, null=True)
    interest_rate = models.CharField(max_length=10, null=True)

"""InterestByRegionFrameworkLibrary(?fw_or_lib, ?region, ?interest_rate)"""
class InterestByRegionFrameworkLibrary(models.Model):
    fw_or_lib = models.CharField(unique=True, max_length=30)
    date = models.CharField(max_length=20, null=True)
    interest_rate = models.CharField(max_length=10, null=True)
"""Course(?course_id, ?slug, ?course_type, ?course_name, ?logo, ?photo_url,
?description, ?workload, ?url)"""
class Course(models.Model):
    course_id = models.CharField(unique=True, max_length=30)
    slug =  models.CharField(max_length=30, null=True)
    course_type =  models.CharField(max_length=30, null=True)
    logo = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    description = models.CharField(max_length=150, null=True)
    workload = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)



"""CoursePartner(?course_id, ?partner_id, ?partner_name, ?partner_image)"""

class CoursePartner(models.Model):
    partner_id = models.CharField(max_length=30, unique= True)
    course_id = models.ManyToManyField(Course, null=True)
    partner_name = models.CharField(max_length=30, null=True)
    partner_image =  models.URLField(null=True)
"""Job(?job_title, ?description, ?post_date, ?company_name, ?company_url,
?location_name, ?lat, ?lon, ?query)"""

class Job(models.Model):
    job_title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150, null=True)
    post_date = models.CharField(max_length=10, null=True)
    company_name = models.CharField(max_length=30, null=True)
    company_url = models.URLField(null=True)
    location_name =  models.CharField(max_length=30, null=True)
    lat =  models.CharField(max_length=30, null=True)
    query =  models.CharField(max_length=30, null=True)

class Suggestion(models.Model):
   keyword = models.CharField(max_length=30)
   suggested_keyword = models.CharField(max_length=30)