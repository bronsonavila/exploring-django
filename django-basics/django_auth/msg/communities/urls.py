from django.urls import path, re_path

from . import views

app_name = 'communities'

urlpatterns = [
    re_path(r"^$", views.AllCommunities.as_view(), name="list"),
    re_path(r"^new/$", views.CreateCommunity.as_view(), name="create"),
    re_path(
        r"^posts/in/(?P<slug>[-\w]+)/$",
        views.SingleCommunity.as_view(),
        name="single"
    ),
    re_path(
        r"join/(?P<slug>[-\w]+)/$",
        views.JoinCommunity.as_view(),
        name="join"
    ),
    re_path(
        r"leave/(?P<slug>[-\w]+)/$",
        views.LeaveCommunity.as_view(),
        name="leave"
    ),
    path(
        'change_status/<slug:slug>/<int:user_id>/<int:status>/',
        views.ChangeStatus.as_view(),
        name='change_status'
    )
]
