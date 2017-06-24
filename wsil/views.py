from django.views.generic import TemplateView, DetailView
from django.shortcuts import render_to_response, get_object_or_404

from wsil.models import LibraryOrFramework, InterestByRegionLanguage
from .models import RepositoryUsingIt, Language, InterestOverTimeFrameworkLibrary, InterestByRegionFrameworkLibrary
from .models import InterestOverTimeLanguage, QuestionOnIt, Job, Course, CoursePartner, Features
from rest_framework import generics
from wsil.serializer import SuggestionSerializer, Top10Serializer, InterestOverTimeSerializer, InterestByRegionSerializer


# Create your views here.


class IndexView(TemplateView):
    template_name = "wsil/index.html"
    title = 'WSIL'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class MainHomeView(TemplateView):
    template_name = "wsil/home.html"
    title = 'WSIL'

    def get_context_data(self, **kwargs):
        context = super(MainHomeView, self).get_context_data(**kwargs)
        lang_count = Language.objects.all().count()
        fw_count = LibraryOrFramework.objects.all().count()
        top10 = [i.language for i in RepositoryUsingIt.objects.all().order_by('-repository_count')[:10]]
        languages = []
        for lang in top10:
            l = Language.objects.get(name__iexact=lang)
            languages.append(l)
        context['top10'] = languages
        context['languagecount'] = lang_count
        context['fwcount'] = fw_count
        return context


class FrameworkDetail(DetailView):
    title = "Framework Detail"
    model = LibraryOrFramework
    template_name = "wsil/fwdetail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        fw_name = context['object'].name
        try:
            details = Features.objects.get(library_framework_name=fw_name)
            fields = [(i.help_text,getattr(details, i.name)) for i in details._meta.fields if len(i.help_text) > 0]
            context['details'] = fields
        except:
            pass
        jobs =  Job.get_all_job_for(fw_name)
        context['jobs'] = jobs if jobs.count() > 0 else []
        courses = Course.get_courses_for_lang(fw_name)
        context['courses'] = courses if courses.count() > 0 else []
        return context




class LanguageDetail(TemplateView):
    template_name = "wsil/language.html"

    def get_context_data(self, **kwargs):
        context = super(LanguageDetail, self).get_context_data(**kwargs)
        id = kwargs['lng']
        language_obj = Language.objects.get(pk=id)
        language_name = language_obj.name
        self.language = get_object_or_404(RepositoryUsingIt, language__iexact=language_name)
        context['l_title'] = language_name
        context['language'] = language_obj
        context['fwls'] = language_obj.libraryorframework_set.all()
        query = context['l_title']
        context['jobs'] = Job.get_all_job_for(query)
        context['question_count'] = QuestionOnIt.get_count_for_lang(query).count
        context['courses'] = Course.get_courses_for_lang(query)
        return context


class JobDetail(DetailView):
    title = "Job Detail"
    model = Job
    template_name = "wsil/job.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context


class CourseDetail(DetailView):
    title = "Course Detail"
    model = Course
    template_name = "wsil/course.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pk = kwargs['object'].course_id
        if kwargs['object'].source == 'COURSERA':
            context['partners'] = CoursePartner.get_course_partner(pk)
        return context

# REST

class SuggestedView(generics.ListAPIView):
    serializer_class = SuggestionSerializer

    def get_queryset(self):
        return Language.objects.filter(name__icontains=self.kwargs['kw']).order_by('name')[:10]


class Top10ForCharts(generics.ListAPIView):
    serializer_class = Top10Serializer

    def get_queryset(self):
        return RepositoryUsingIt.objects.all().order_by('-repository_count')[:10]


class InterestOverTimeLang(generics.ListAPIView):
    serializer_class = InterestOverTimeSerializer

    def get_queryset(self):
        language_name = Language.objects.get(pk=self.kwargs['pk']).name
        print(language_name)
        lan = InterestOverTimeLanguage.objects.filter(language_name__iexact=language_name).order_by('date')
        return lan


class InterestByRegionLang(generics.ListAPIView):
    serializer_class = InterestByRegionSerializer

    def get_queryset(self):
        language_name = Language.objects.get(pk=self.kwargs['pk']).name
        lan = InterestByRegionLanguage.objects.filter(language__iexact=language_name).order_by('region')
        return lan


class InterestOverTimeFw(generics.ListAPIView):
    serializer_class = InterestOverTimeSerializer

    def get_queryset(self):
        framework_name = LibraryOrFramework.objects.get(pk=self.kwargs['pk']).name
        fwdata = InterestOverTimeFrameworkLibrary.objects.filter(fw_or_lib__iexact=framework_name).order_by('date')
        return fwdata


class InterestByRegionFw(generics.ListAPIView):
    serializer_class = InterestByRegionSerializer

    def get_queryset(self):
        fwname = LibraryOrFramework.objects.get(pk=self.kwargs['pk']).name
        fwdata = InterestByRegionFrameworkLibrary.objects.filter(fw_or_lib__iexact =fwname).order_by('region')
        return fwdata

