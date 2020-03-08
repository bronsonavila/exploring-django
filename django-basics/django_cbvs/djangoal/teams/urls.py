from django.urls import re_path

from . import views

app_name = 'teams'

urlpatterns = [
    re_path(r'^$', views.team_list, name='list'),
    re_path(r'^(?P<pk>\d+)/$', views.team_detail, name='detail'),
]
