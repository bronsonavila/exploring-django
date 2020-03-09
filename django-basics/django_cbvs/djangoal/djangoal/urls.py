"""djangoal URL Configuration

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

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('teams/', include('teams.urls', namespace='teams')),
    # The `HelloWorldView` must call the `as_view()` method because it is based
    # on the `View` class. The `as_view()` method creates an instance of the
    # class, configures the request object, and runs the class's dispatch
    # method. The dispatch method runs the correct class method based on the
    # incoming HTTP request (i.e., if the HTTP request is a `GET` request,
    # then the dispatch method with call the class's `get()` method).
    path('hello/', views.HelloWorldView.as_view(), name='hello')
]
