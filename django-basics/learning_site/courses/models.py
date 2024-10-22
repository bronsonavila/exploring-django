from django.urls import reverse
from django.db import models

# Django's built-in "User" model can be used when authentication is required.
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('i', 'In Progress'),
    ('r', 'In Review'),
    ('p', 'Published'),
)

# The Course class inherits from `models.Model`.
class Course(models.Model):
    # Set value automatically to current time when a record is first created.
    # The current time is determined by the `TIME_ZONE` value in `settings.py`.
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    subject = models.CharField(default='', max_length=100)
    published = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')

    # "Dunder string" defines how an instance is turned into a string. This is
    # used when Django prints a reference to an instance (e.g., in the shell).
    # Can return something more informative than <Course: Course object (3)>.
    def __str__(self):
        return self.title

    def time_to_complete(self):
        # Must import `course_extras` within this method rather than at the top
        # of the file because `course_extras` imports the `Course` model as a
        # dependency. Importing `course_extras` at the top of this file (before
        # the `Course` model is declared) will lead to a recursive import error.
        from courses.templatetags.course_extras import time_estimate
        return '{} min'.format(time_estimate(len(self.description.split())))


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    # Establish a many-to-one relationship where many steps belong to one course.
    # If the Course class appeared after Step, then "Course" must be in quotes.
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,  # Delete child tables.
    )

    # Django models have the `Meta` class as an option to control
    # the model's behavior.
    class Meta:
        # Define the class as `abstract` if it will be used only for inheritance.
        abstract = True
        # Order all records by the `order` attribute, and then
        # fall back to using the `id` if the same `order` is used.
        ordering = ['order', ]

    def __str__(self):
        return self.title


class Text(Step):
    # `blank` refers to the form in the admin menu (i.e., allowed to be empty).
    content = models.TextField(blank=True, default='')

    def get_absolute_url(self):
        return reverse('courses:text', kwargs={'course_pk': self.course_id, 'step_pk': self.id})


class Quiz(Step):
    total_questions = models.IntegerField(default=4)
    times_taken = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def get_absolute_url(self):
        return reverse('courses:quiz', kwargs={'course_pk': self.course_id, 'step_pk': self.id})


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )
    order = models.IntegerField(default=0)
    prompt = models.TextField()

    class Meta:
        ordering = ['order', ]

    # Makes it easier to get to specific model instances, and can also
    # be useful in the admin view (for creating a "View on Site" button).
    def get_absolute_url(self):
        return self.quiz.get_absolute_url()

    def __str__(self):
        return self.prompt


class MultipleChoiceQuestion(Question):
    shuffle_answers = models.BooleanField(default=False)


class TrueFalseQuestion(Question):
    pass


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    order = models.IntegerField(default=0)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.text
