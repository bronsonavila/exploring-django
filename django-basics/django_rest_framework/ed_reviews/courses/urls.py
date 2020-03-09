from django.urls import path, include

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.ListCourse.as_view(), name='course_list'),
]
