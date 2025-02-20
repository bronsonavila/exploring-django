from django.urls import re_path

from . import views

app_name = 'posts'

urlpatterns = [
    re_path(r"^$", views.AllPosts.as_view(), name="all"),
    re_path(r"new/$", views.CreatePost.as_view(), name="create"),
    re_path(
        # NOTE: If this type of logic is used in production, ensure that user
        # cannot create a username that contains a space. This regex test does
        # not allow space characters, and an error will occur if one exists.
        r"by/(?P<username>[-\w]+)/$",
        views.UserPosts.as_view(),
        name="for_user"
    ),
    re_path(
        r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",
        views.SinglePost.as_view(),
        name="single"
    ),
    re_path(
        r"delete/(?P<pk>\d+)/$",
        views.DeletePost.as_view(),
        name="delete"
    ),
]
