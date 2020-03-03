from django import forms

from . import models


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        # Specify the fields you want to include.
        fields = [
            'title',
            'description',
            'order',
            'total_questions',
        ]


class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = [
            'order',
            'prompt',
        ]


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = [
            'order',
            'prompt',
            'shuffle_answers',
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = [
            'order',
            'text',
            'correct',
        ]


AnswerFormset = forms.modelformset_factory(
    models.Answer,
    form=AnswerForm,
    extra=2,  # Show 2 extra blank sets of form inputs (default=1)
)


AnswerInlineFormset = forms.inlineformset_factory(
    models.Question,  # The model that will contain the inline form.
    models.Answer,  # The model to be editted in the inline form.
    extra=2,
    fields=('order', 'text', 'correct'),
    formset=AnswerFormset,  # Per lecturer: "Not required."
    min_num=1,
)
