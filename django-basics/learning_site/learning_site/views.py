from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


# All views must accept a `request` parameter, even if not actually used.
def home(request):
    return render(request, 'home.html')


def suggestion_view(request):
    form = forms.SuggestionForm()

    if request.method == 'POST':
        # Pass in the form data via the `request.POST` dictionary,
        # and then validate the form's inputs in relation to the class.
        # This is a "time-tested" approach to handling form validation.
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            # After being run through the `is_valid()` method, each field
            # will be added to the `cleaned_data` object.
            send_mail(
                'Suggestion from {}'.format(form.cleaned_data['name']),
                form.cleaned_data['suggestion'],
                '{name} <{email}>'.format(**form.cleaned_data),
                ['name@email.com']
            )
            # Display flash message on the screen after submission.
            messages.add_message(request, messages.SUCCESS,
                                 'Thanks for your suggestion!')
            # Redirect to the same page (acts as a way to clear the form).
            return HttpResponseRedirect(reverse('suggestion'))

    return render(request, 'suggestion_form.html', {'form': form})
