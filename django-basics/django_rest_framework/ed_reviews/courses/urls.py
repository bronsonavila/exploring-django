from django.urls import path, include

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.ListCreateCourse.as_view(), name='course_list'),
    # `RetrieveUpdateDestroyAPIView` expects a query parameter called `pk`.
    path('<pk>/', views.RetrieveUpdateDestroyCourse.as_view(), name='course_detail')
]
