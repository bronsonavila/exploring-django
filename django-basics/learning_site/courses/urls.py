from django.urls import path, register_converter

from . import converters, views

# Must include an app name for namespacing to work.
app_name = 'courses'

# Evaluate `question_type` query parameter with regex.
register_converter(converters.QuestionType, 'question')

urlpatterns = [
    # Place step_detail above course_detail to ensure that the course detail
    # is not rendered when attempting to access a step detail.
    path('', views.course_list, name='list'),
    path('<int:course_pk>/t<int:step_pk>/', views.text_detail, name='text'),
    path('<int:course_pk>/q<int:step_pk>/', views.quiz_detail, name='quiz'),
    path('<int:course_pk>/create_quiz/', views.quiz_create, name='create_quiz'),
    path('<int:course_pk>/edit_quiz/<int:quiz_pk>/', views.quiz_edit, name='edit_quiz'),
    path('<int:quiz_pk>/create_question/<question:question_type>', views.create_question, name='create_question'),
    path('<int:quiz_pk>/edit_question/<int:question_pk>/', views.edit_question, name='edit_question'),
    path('<int:question_pk>/create_answer/', views.answer_form, name='create_answer'),
    path('<int:pk>/', views.course_detail, name='detail'),
]
