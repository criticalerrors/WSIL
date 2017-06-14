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



"""QuestionOnIt(?tag, ?count)"""

"""InterestOverTimeLanguage(?language_name, ?date, ?interest_rate)"""

"""InterestOverTimeFrameworkLibrary(?fw_or_lib, ?date, ?interest_rate)"""

""" InterestByRegionLanguage(?language, ?region, ?interest_rate)"""

"""InterestByRegionFrameworkLibrary(?fw_or_lib, ?region, ?interest_rate)"""

"""Course(?course_id, ?slug, ?course_type, ?course_name, ?logo, ?photo_url,
?description, ?workload, ?url)"""

"""CoursePartner(?course_id, ?partner_id, ?partner_name, ?partner_image)"""

"""Job(?job_title, ?description, ?post_date, ?company_name, ?company_url,
?location_name, ?lat, ?lon, ?query)"""

"""Suggestion(?keyword, ?suggested_keyword):-"""