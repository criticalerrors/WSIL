from django.conf.urls import url
from django.conf.urls import handler404
from . import views

handler404 = views.handler404

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.MainHomeView.as_view(), name='main_home'),
    url(r'^details/(?P<lng>[0-9]+)$', views.LanguageDetail.as_view(), name='detail_lang'),
    url(r'^job/(?P<pk>[0-9]+)$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^about/$', views.MainHomeView.as_view(), name='about_page'), #todo
    url(r'^api/suggest/(?P<kw>[a-z]+)$', views.SuggestedView.as_view(), name="suggestion_api"),
    url(r'^api/top10/$', views.Top10ForCharts.as_view(), name="top10charts"),
    url(r'^api/interest_time/(?P<lng>[a-z]+)$', views.InterestOverTimeLang.as_view(), name="iot_lang")
]
