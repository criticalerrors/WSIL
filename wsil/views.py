from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.


class IndexView(TemplateView):
    template_name = "wsil/index.html"
    title = 'Your title'

    def get_context_data(self, **kwargs):
        props = {
            'example_list': [
                {'key': 'value1'},
                {'key': 'value2'},
            ]
        }
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['props'] = props
        return context


class MainHomeView(TemplateView):
    template_name = "wsil/home.html"
    title = 'Your title'

    def get_context_data(self, **kwargs):
        props = {
            'example_list': [
                {'key': 'value1'},
                {'key': 'value2'},
            ]
        }
        context = super(MainHomeView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['props'] = props
        return context

def handler404(request):
    response = render_to_response('wsil/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response