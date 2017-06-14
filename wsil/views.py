from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import RepositoryUsingIt

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


def handler404(request):
    response = render_to_response('wsil/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response