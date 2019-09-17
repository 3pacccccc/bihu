# __author__ = "MaRuiMin"
from django.urls import path

from qa import views

app_name = 'qa'

urlpatterns = [
    path('', views.UnansweredQuestionsListView.as_view(), name='unanswered_q'),
    path('answered/', views.AnsweredQuestionsListView.as_view(), name='answered_q'),
    path('indexed', views.QuestionListView.as_view(), name='all_q')
]