from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('random/', views.random_quiz, name='random_quiz'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/question/<int:question_number>/', views.quiz_question, name='quiz_question'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/timeout/', views.quiz_timeout, name='quiz_timeout'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]