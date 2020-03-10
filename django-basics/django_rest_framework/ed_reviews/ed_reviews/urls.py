"""ed_reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin

from rest_framework import routers

from courses import views

router = routers.SimpleRouter()
# Register viewsets with the router, and assign a prefix.
router.register(r'courses', views.CourseViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Include API version number.
    path('api/v1/courses/', include('courses.urls', namespace='courses')),
    # Create URLs automatically for each viewset registered with the router.
    path('api/v2/', include((router.urls, 'ed_reviews'), namespace='apiv2')),
]
