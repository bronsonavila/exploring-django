from itertools import chain

from django.contrib import messages
# Marks a view as requiring a logged-in user.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import forms
from . import models


def course_list(request):
    courses = models.Course.objects.filter(published=True)
    email = 'questions@learning_site.com'
    # This `render()` has three arguments: (1) request, (2) template path, and
    # (3) context dictionary. The first two are always required.
    return render(request, 'courses/course_list.html', {'courses': courses, 'email': email})


# Django automatically provides `request`, and we provide the
# primary key (the ID, by default) through the URL.
def course_detail(request, pk):
    # Show 404 if the Course object is not found.
    course = get_object_or_404(models.Course, pk=pk, published=True)
    # Get all text and quiz steps, combine them, and sort by `order` attribute.
    # `text_set` is a query set that can be queried against for all `text` records
    # belonging to a course.
    steps = sorted(chain(course.text_set.all(),
                         course.quiz_set.all()), key=lambda step: step.order)
    return render(request, 'courses/course_detail.html', {'course': course, 'steps': steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text,
                             course_id=course_pk,
                             pk=step_pk,
                             course__published=True)
    return render(request, 'courses/step_detail.html', {'step': step})


def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz,
                             course_id=course_pk,
                             pk=step_pk,
                             course__published=True)
    return render(request, 'courses/step_detail.html', {'step': step})


@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(
        models.Course, pk=course_pk, course__published=True)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            # `commit=False` means "don't actually put this in the database,
            # just make the model instance and hold it in memory."
            # This allows you to modify the form data before saving.
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS, 'Quiz added!')
            return HttpResponseRedirect(quiz.get_absolute_url())

    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})


@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz,
                             pk=quiz_pk,
                             course_id=course_pk,
                             course__published=True)
    form = forms.QuizForm(instance=quiz)

    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(
                form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())

    return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':
        # Just define the class; do not instantiate it, as the manner of
        # instantiation will differ for GET and POST requests.
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()
    answer_forms = forms.AnswerInlineFormset(
        # The question has no answers since it's just being created,
        # so you must pull in a blank queryset.
        queryset=models.Answer.objects.none()
    )

    if request.method == 'POST':
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormset(
            request.POST,
            queryset=models.Answer.objects.none(),
        )

        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, 'Added question')
            return HttpResponseRedirect(quiz.get_absolute_url())

    return render(request, 'courses/question_form.html', {
        'quiz': quiz,
        'form': form,
        'formset': answer_forms,
    })


@login_required
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(
        models.Question, pk=question_pk, quiz_id=quiz_pk)

    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion

    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormset(
        queryset=form.instance.answer_set.all()
    )

    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormset(
            request.POST,
            queryset=form.instance.answer_set.all()
        )

        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            # If you use `commit=False`, objects will not be deleted
            # automatically. You must call `delete()` on each object.
            for answer in answer_forms.deleted_objects:
                answer.delete()
            messages.success(request, 'Updated question')
            return HttpResponseRedirect(question.quiz.get_absolute_url())

    return render(request, 'courses/question_form.html', {
        'quiz': question.quiz,
        'form': form,
        'formset': answer_forms,
    })


@login_required
def answer_form(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    formset = forms.AnswerFormset(queryset=question.answer_set.all())

    if request.method == 'POST':
        formset = forms.AnswerFormset(
            request.POST, queryset=question.answer_set.all())
        if formset.is_valid():
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, 'Added answers')
            return HttpResponseRedirect(question.quiz.get_absolute_url())

    return render(request, 'courses/answer_form.html', {
        'formset': formset,
        'question': question,
    })


def courses_by_teacher(request, teacher):
    # teacher = models.User.objects.get(username=teacher)
    # courses = teacher.course_set.all()

    # Simpler way to query courses by teacher, rather than using the
    # commented out code above. This method is also preferred because
    # it will just produce an empty queryset rather than a 404 error
    # if the given teacher name does not exist in the database.
    courses = models.Course.objects.filter(
        teacher__username=teacher, published=True)

    return render(request, 'courses/course_list.html', {'courses': courses})


def search(request):
    term = request.GET.get('q')
    # Get courses where the title contains the term (case insensitive).
    courses = models.Course.objects.filter(
        title__icontains=term, published=True)
    return render(request, 'courses/course_list.html', {'courses': courses})
