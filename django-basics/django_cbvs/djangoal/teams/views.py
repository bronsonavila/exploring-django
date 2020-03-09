from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from . import models


def team_list(request):
    teams = models.Team.objects.all()
    return render(request, 'teams/team_list.html', {'teams': teams})


def team_detail(request, pk):
    team = get_object_or_404(models.Team, pk=pk)
    return render(request, 'teams/team_detail.html', {'team': team})


class TeamListView(ListView):
    model = models.Team
    # By default, Django sets the context name of the list to be generated
    # as both `object_list` and the lower-cased version of the model class's
    # name followed by `_list` (in this case, `team_list`). However, it you
    # want to change that name to something else, use `context_object_name`.
    context_object_name = 'teams'


class TeamDetailView(DetailView):
    model = models.Team


class TeamCreateView(CreateView):
    model = models.Team
    fields = ('name', 'practice_location', 'coach')

    # `get_initial` populates a form with starter data. Here, the form
    # will begin with the logged-in user assigned as the coach.
    def get_initial(self):
        initial = super().get_initial()
        initial['coach'] = self.request.user.pk
        return initial


class TeamUpdateView(UpdateView):
    model = models.Team
    fields = ('name', 'practice_location', 'coach')


class TeamDeleteView(DeleteView):
    model = models.Team
    # `reverse_lazy` is evaluated when the view is instantiated (as opposed to
    # `reverse`, which is evaluated when this file is read & parsed by Python).
    # So it won't matter if the URL for the list view doesn't exist yet when
    # the file is read.
    success_url = reverse_lazy('teams:list')

    # Override the default `get_queryset` method to say that only a superuser
    # can delete any team. Otherwise, a user can only delete teams for which
    # the user is a coach.
    def get_queryset(self):
        # All class-based views have a `request` attribute.
        if not self.request.user.is_superuser:
            return self.model.objects.filter(coach=self.request.user)
        return self.model.objects.all()
