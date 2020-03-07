# The `template` module contains the function required to register
# templates. When you register a template tag, you are making the
# tag available to Django's template language for future use.
from django import template
from django.utils.safestring import mark_safe

import markdown2

from courses.models import Course


register = template.Library()

# Course notes: Simple tags don't include new templates, don't have
# an end tag, and don't assign values to context variables.
@register.simple_tag
def newest_course():
    """Gets the most recent course that was added to the library."""
    return Course.objects.filter(published=True).latest('created_at')

# If you do not include the `@register` decorator, this line would
# be required to register the template tag:
# register.simple_tag(newest_course)

@register.inclusion_tag('courses/course_nav.html')
def nav_courses_list():
    """Returns dictionary of courses to display as navigation pane."""
    courses = Course.objects.filter(published=True)
    return {'courses': courses}

@register.filter
def time_estimate(word_count):
    """Estimates the number of minutes to complete a step."""
    minutes = round(word_count/20)
    return minutes

@register.filter
def markdown_to_html(markdown_text):
    """Converts Markdown text to HTML."""
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)
