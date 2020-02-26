from django.urls import path

from . import views

# Must include an app name for namespacing to work.
app_name = 'courses'

urlpatterns = [
    # Place step_detail above course_detail to ensure that the course detail
    # is not rendered when attempting to access a step detail.
    path('', views.course_list, name='list'),
    path('<int:course_pk>/t<int:step_pk>/', views.text_detail, name='text'),
    path('<int:course_pk>/q<int:step_pk>/', views.quiz_detail, name='quiz'),
    path('<int:pk>/', views.course_detail, name='detail'),
]
