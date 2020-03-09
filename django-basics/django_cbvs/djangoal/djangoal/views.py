from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView


def home(request):
    return render(request, 'home.html')


class HomeView(TemplateView):
    template_name = 'home.html'

    # Gets/generates context dictionary that's used for rendering template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add hardcoded value that's accessible to the template.
        context['games_today'] = 6
        return context


class HelloWorldView(View):
    # Each view based on the `View` class accepts the `get()` method.
    def get(self, request):
        return HttpResponse('Hello World')
