from django.shortcuts import get_object_or_404, render

from .models import Course, Step


def course_list(request):
    courses = Course.objects.all()
    email = 'questions@learning_site.com'
    # This `render()` has three arguments: (1) request, (2) template path, and
    # (3) context dictionary. The first two are always required.
    return render(request, 'courses/course_list.html', {'courses': courses, 'email': email})


# Django automatically provides `request`, and we provide the
# primary key (the ID, by default) through the URL.
def course_detail(request, pk):
    # Show 404 if the Course object is not found.
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


def step_detail(request, course_pk, step_pk):
    step = get_object_or_404(Step, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/step_detail.html', {'step': step})
