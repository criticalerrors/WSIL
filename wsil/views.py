from django.views.generic import TemplateView, DetailView
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from .models import RepositoryUsingIt, Language
from .models import InterestOverTimeLanguage, QuestionOnIt, Job, Course
from rest_framework import generics
from wsil.serializer import SuggestionSerializer, Top10Serializer, InterestOverTimeSerializer


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
        top10 = [i.language for i in RepositoryUsingIt.objects.all().order_by('-repository_count')[:10]]
        languages = []
        for lang in top10:
            l = Language.objects.get(name__iexact=lang)
            languages.append(l)
        context['top10'] = languages
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
        context['jobs_count'] = Job.get_all_job_for(query).count()
        context['jobs'] = Job.get_all_job_for(query)
        context['question_count'] = QuestionOnIt.get_count_for_lang(query).count
        context['courses'] = Course.get_courses_for_lang(query)
        return context


class JobDetail(DetailView):
    model = Job
    template_name = "wsil/job.html" # TODO


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
