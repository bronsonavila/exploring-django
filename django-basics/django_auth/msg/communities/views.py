from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import PrefetchRelatedMixin

from . import models


class CreateCommunity(generic.CreateView):
    fields = ("name", "description")
    model = models.Community

    def form_valid(self, form):
        resp = super().form_valid(form)
        models.CommunityMember.objects.create(
            community=self.object,
            user=self.request.user,
            role=3
        )
        return resp


class SingleCommunity(PrefetchRelatedMixin, generic.DetailView):
    model = models.Community
    prefetch_related = ("members",)


class AllCommunities(generic.ListView):
    model = models.Community


class JoinCommunity(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("communities:single",
                       kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        community = get_object_or_404(models.Community,
                                      slug=self.kwargs.get("slug"))
        try:
            models.CommunityMember.objects.create(
                user=self.request.user,
                community=community,
                role=1
            )
        except IntegrityError:
            messages.warning(
                self.request,
                ("You were already a member of <b>{}</b>.  "
                 "Don't be sneaky!").format(
                    community.name
                )
            )
        else:
            messages.success(
                self.request,
                "You're now a member of <b>{}</b>!".format(community.name)
            )
        return super().get(request, *args, **kwargs)


class LeaveCommunity(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("communities:single",
                       kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.CommunityMember.objects.filter(
                user=self.request.user,
                community__slug=self.kwargs.get("slug")
            ).exclude(role=3).get()
        except models.CommunityMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You've left the group!"
            )
        return super().get(request, *args, **kwargs)
