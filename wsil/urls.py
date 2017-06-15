from django.conf.urls import url
from django.conf.urls import handler404
from . import views

handler404 = views.handler404

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.MainHomeView.as_view(), name='main_home'),
    url(r'^api/suggest/(?P<kw>[a-z]+)$', views.SuggestedView.as_view(), name="suggestion_api"),
    url(r'^api/top10/$', views.Top10ForCharts.as_view(), name="top10charts")
]
