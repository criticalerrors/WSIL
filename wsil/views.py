from django.views.generic import TemplateView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Avg
from .models import RepositoryUsingIt, Language, InterestOverTimeFrameworkLibrary, LibraryOrFramework
from .models import InterestOverTimeLanguage, QuestionOnIt, Job, Course
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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
        context['top10'] = RepositoryUsingIt.objects.all().order_by('-repository_count')[:10]
        return context


class LanguageDetail(TemplateView):
    template_name = "wsil/language.html"

    def get_context_data(self, **kwargs):
        context = super(LanguageDetail, self).get_context_data(**kwargs)
        id = kwargs['lng']
        context['l_title'] = RepositoryUsingIt.objects.get(pk=id).language
        context['top10fwl'] = [] # TODO
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
        return InterestOverTimeLanguage.objects.filter(language_name__iexact=self.kwargs['lng']).order_by('date')


def handler404(request):
    response = render_to_response('wsil/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response