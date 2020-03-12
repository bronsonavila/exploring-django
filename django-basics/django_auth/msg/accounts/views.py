from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic


# NOTE: This view is not currently in use.
# `django.contrib.auth.urls` is being used for the login view instead.
class LoginView(generic.FormView):
    # Ensure the user is authenticated before attemping a log in.
    form_class = AuthenticationForm
    # Redirect when the form view is complete.
    success_url = reverse_lazy('posts:all')
    template_name = 'accounts/login.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        # The default `form_class` just takes the second argument,
        # but the first argument in an `AuthenticationForm` must
        # be the request.
        return form_class(self.request, **self.get_form_kwargs())

    # Only login if the `AuthenticationForm` is valid.
    def form_valid(self, form):
        # `self.request` is used in creating the session and validating
        # that a request is coming from the user. The `form.get_user()`
        # method is a method provided by the `AuthenticationForm` which
        # returns the authenticated user object.
        login(self.request, form.get_user())
        return super().form_valid(form)