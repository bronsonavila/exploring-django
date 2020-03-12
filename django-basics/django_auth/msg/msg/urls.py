"""msg URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('admin/', admin.site.urls),
    # This first `accounts/` path should only contain URLs that
    # go beyond those provided by `django.contrib.auth.urls`. This
    # means `account.urls` should not contain a `login/` path, because
    # `django.contrib.auth.urls` already contains such a path.
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # This path will only be executed if there are no matches
    # for any URLs in the `accounts` path above.
    path('accounts/', include('django.contrib.auth.urls')),
    path('posts/', include("posts.urls", namespace="posts")),
    path('communities/', include("communities.urls", namespace="communities")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
