# NOTE: You cannot use `django.conf import settings` for the `Meta` model.
# `settings.AUTH_USER_MODEL` only returns a string, but you need an actual
# model object. The `get_user_model` method makes that happen here, as it
# always returns the "active" user model (which, in this case, will be the
# `AUTH_USER_MODEL` defined in `settings.py`).
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        model = get_user_model()

    # Override the default form labels.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display name'
        # NOTE: The `email` field of Django's `User` model is optional.
        # If you need it to be required, this class will need
        # to be customized further.
        # Google: django usercreationform email
        self.fields['email'].label = 'Email address'
