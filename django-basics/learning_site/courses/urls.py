from django.urls import path

from . import views

# Must include an app name for namespacing to work.
app_name = 'courses'

urlpatterns = [
    # Place step_detail above course_detail to ensure that the course detail
    # is not rendered when attempting to access a step detail.
    path('', views.course_list, name='list'),
    path('<int:course_pk>/<int:step_pk>/', views.step_detail, name='step'),
    path('<int:pk>/', views.course_detail, name='detail'),
]
