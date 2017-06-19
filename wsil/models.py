from django.db import models
from django.utils import timezone
from xml.etree import ElementTree
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
        if in_db.count() > 0:
            in_db = in_db[0]
            if in_db.cache_date > timezone.now():
                print("Cached!")
                return in_db
            else:
                t = threading.Thread(target=clear_cache, args=(QuestionOnIt,))
                t.start()
        url = "https://api.stackexchange.com/2.2/tags?order=desc&sort=popular&inname="+lang.lower()+"&site=stackoverflow"
        json = get_url_req(url)['items']
        for tag in json:
            if lang.lower() == tag['name'].lower():
                try:
                    tc = cls(tag=lang, count=tag['count'] if 'count' in tag else 0)
                    if t:
                        t.join()
                    tc.save()
                    return tc
                except Exception as ex:
                    print(ex)
        not_found = cls(tag=lang, count=0)
        not_found.save()
        return not_found


class Language(models.Model):
    name = models.CharField(unique=True, max_length=30)


class LibraryOrFramework(models.Model):
    name = models.CharField(unique=True, max_length=40)
    type = models.CharField(max_length=30, null=True)
    initial_release = models.CharField(max_length=100, null=True)
    stable_release = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=50,null= True)
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
    course_id = models.CharField(max_length=30, primary_key=True)
    slug = models.CharField(max_length=30, null=True)
    course_type = models.CharField(max_length=30, null=True)
    logo = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    description = models.CharField(max_length=150, null=True)
    workload = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)
    cache_date = models.DateTimeField(null=True, default=tomorrow)
    source = models.CharField(null=False, max_length=10, default="COURSERA")

    @classmethod
    def get_courses_for_lang(cls, lang):
        t = None
        in_db = cls.objects.filter(description__contains=lang).filter(cache_date__gt=timezone.now())
        if len(in_db) != 0:
            return in_db
        t = threading.Thread(target=clear_cache, args=(Course,))
        t.start()
        courses = []
        # COURSERA
        url = "https://api.coursera.org/api/courses.v1?q=search&query="+lang+"&fields=partnerLogo,photoUrl,description,workload,previewLink"
        json = get_url_req(url)
        for course in json['elements']:
            try:
                c = cls(course_id=course['id'], slug=course['slug'], course_type=course['courseType'], logo=course['partnerLogo'],
                        photo_url=course['photoUrl'], description=course['description'], workload=course['workload'],
                        url='https://www.coursera.org/', source="COURSERA")
                courses.append(c)
            except Exception as ex:
                print("Missing data in Coursera")
                print(ex)
        # UDACITY
        if cls.objects.filter(source="UDACITY").count() != 0:
            t.join()
            cls.objects.bulk_create(courses)
            return cls.objects.filter(description__contains=lang).filter(cache_date__gt=timezone.now())

        url = "https://www.udacity.com/public-api/v1/courses"
        json = get_url_req(url)
        for course in json['courses']:
            if not course['available']:
                continue
            try:
                c = cls(course_id=course['key'], slug=course['slug'], course_type=course['level'], logo=course['banner_image'],
                        photo_url=course['image'], description=course['summary'],
                        workload=str(course['expected_duration']) + " " + course['expected_duration_unit'],
                        url='https://www.udacity.com', source="UDACITY")
                courses.append(c)
            except Exception as ex:
                print("Missing data in Udacity")
                print(ex)
        t.join()
        print(courses)
        cls.objects.bulk_create(courses)
        return courses


class CoursePartner(models.Model):
    partner_id = models.CharField(max_length=30, unique=True)
    course_id = models.CharField(max_length=30, null=True)
    partner_name = models.CharField(max_length=30, null=True)
    partner_shortname = models.CharField(null=True, max_length=5)

    @classmethod
    def get_course_partner(cls, course_id):
        partner = cls.objects.filter(course_id=course_id)
        if partner.count() != 0:
            return partner
        url = "https://api.coursera.org/api/courses.v1/"+ course_id +"?includes=partnerIds"
        json = get_url_req(url)
        if 'linked' in json and 'partners.v1' in json['linked']:
            for partner in json['linked']['partners.v1']:
                print(partner)
                c = Course.objects.filter(pk=course_id)
                p = cls(partner_id=str(partner['id']), partner_name=partner['name'], partner_shortname=partner['shortName'], course_id=c)
                p.save()
                return p


class Job(models.Model):
    job_title = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True)
    post_date = models.CharField(max_length=10, null=True)
    company_name = models.CharField(max_length=30, null=True)
    company_url = models.URLField(null=True)
    location_name = models.CharField(max_length=30, null=True)
    lang = models.CharField(max_length=3, null=True)
    query = models.CharField(max_length=30, null=True)
    cache_date = models.DateTimeField(null=True, default=tomorrow)

    @classmethod
    def get_all_job_for(cls, lang):
        t = None
        in_db = cls.objects.filter(description__contains=lang).filter(cache_date__gt=timezone.now())
        if len(in_db) != 0:
            return in_db
        t = threading.Thread(target=clear_cache, args=(Job,))
        t.start()
        # INDEED
        url = "http://api.indeed.com/ads/apisearch?publisher=6284576268691023&q=" + lang + "&v=2"
        jobs = get_url_xml(url, 'results/result')
        jobs_list = []
        for job in jobs:
            try:
                j = Job(job_title=job['jobtitle'], description=job['snippet'], post_date=job['date'],
                        company_name=job['company'], company_url=job['url'], location_name=job['city'],
                        lang=job['language'], query=lang)
                jobs_list.append(j)
            except Exception as ex:
                print("Missing values")
                continue
        # AUTH JOBS
        url = "https://authenticjobs.com/api/?api_key=6ee025bd66be61be4bb601e8dd75707c&method=aj.jobs.search&keywords=" + lang
        jobs = get_url_xml_auth_jobs(url)
        for job in jobs:
            try:
                j = Job(job_title=job['title'], description=job['description'], post_date=job['post_date'],
                        company_name=job['company'], company_url=job['url'], location_name=job['city'],
                        lang=job['language'], query=lang)
                jobs_list.append(j)
            except Exception as ex:
                print("Missing values")
                continue
        t.join()
        Job.objects.bulk_create(jobs_list)
        return jobs_list


def clear_cache(model):
    print("Lazy delete")
    model.objects.filter(cache_date__lt=timezone.now()).delete()


def get_url_req(url):
    try:
        r = requests.get(url)
        json = r.json()
        return json
    except ConnectionError as ex:
        print(ex)
    except Exception as ex:
        print(ex)


def get_url_xml(url, query):
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    el_list = []
    for els in tree.findall(query):
        el_dic = {}
        for el in els:
            el_dic[el.tag] = el.text
        el_list.append(el_dic)
    return el_list


def get_url_xml_auth_jobs(url):
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    el_list = []
    for els in tree.findall('listings/listing'):
        el_dic = {}
        try:
            el_dic['title'] = els.attrib['title']
            el_dic['description'] = els.attrib['description']
            el_dic['post_date'] = els.attrib['post_date']

            company = els.find('company')
            el_dic['company'] = company.attrib['name']
            el_dic['url'] = company.attrib['url']

            location_child = els.find('company/location')
            el_dic['city'] = location_child.attrib['name']
            el_dic['language'] = location_child.attrib['country'] if 'country' in location_child.attrib else '-'

            el_list.append(el_dic)
        except AttributeError as ex:
            print("Missing value")
            continue
    return el_list

