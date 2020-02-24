from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step


class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="LEarn to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)


class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())


class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )
        self.course2 = Course.objects.create(
            title="New Course",
            description="A new course"
        )
        self.step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )

    # Test course list view to ensure it shows both courses above.
    def test_course_list_view(self):
        # When testing views, you can use `self.client`, which allows you to
        # make HTTP requests to a URL and fetch the status code and HTML that
        # come from that URL.
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        # `resp` (response) object has an attributed named `context` which is
        # a dictionary of all values passed into the template upon render.
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(
            reverse('courses:detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])

    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step', kwargs={
                               'course_pk': self.course.pk, 'step_pk': self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
