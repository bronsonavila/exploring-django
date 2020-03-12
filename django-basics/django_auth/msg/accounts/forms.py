from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        model = User

    # Override the default form labels.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display name'
        # NOTE: The `email` field of Django's `User` model is optional.
        # If you need it to be required, this class will need
        # to be customized further.
        # Google: django usercreationform email
        self.fields['email'].label = 'Email address'
