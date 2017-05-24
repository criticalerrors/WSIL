from django.conf.urls import url
from django.conf.urls import handler404
from . import views

handler404 = views.handler404

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.MainHomeView.as_view(), name='main_home')
]