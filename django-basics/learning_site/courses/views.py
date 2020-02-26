from itertools import chain

from django.shortcuts import get_object_or_404, render

from . import models


def course_list(request):
    courses = models.Course.objects.all()
    email = 'questions@learning_site.com'
    # This `render()` has three arguments: (1) request, (2) template path, and
    # (3) context dictionary. The first two are always required.
    return render(request, 'courses/course_list.html', {'courses': courses, 'email': email})


# Django automatically provides `request`, and we provide the
# primary key (the ID, by default) through the URL.
def course_detail(request, pk):
    # Show 404 if the Course object is not found.
    course = get_object_or_404(models.Course, pk=pk)
    # Get all text and quiz steps, combine them, and sort by `order` attribute.
    # `text_set` is a query set that can be queried against for all `text` records
    # belonging to a course.
    steps = sorted(chain(course.text_set.all(),
                         course.quiz_set.all()), key=lambda step: step.order)
    return render(request, 'courses/course_detail.html', {'course': course, 'steps': steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/step_detail.html', {'step': step})


def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/step_detail.html', {'step': step})
