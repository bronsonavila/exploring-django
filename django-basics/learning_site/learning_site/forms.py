from django import forms
from django.core import validators


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Please verify your email address.')
    # Specify the `TextArea` widget; otherwise, it will be an input field.
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        validators=[must_be_empty]
    )

    # If a method is named `clean`, then it will clean the entire form.
    # Django will go through each field and make sure they satisfy
    # their own requirements. Then Django will look a the form as a whole
    # to make sure the form follows the `clean` method's requirements.
    def clean(self):
        # `super().clean()` preserves validation logic in parent classes.
        # See: https://docs.djangoproject.com/en/3.0/ref/forms/validation/
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise forms.ValidationError('Email fields must match.')
