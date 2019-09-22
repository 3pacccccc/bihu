# __author__ = "MaRuiMin"
from django.urls import path

from messager import views

app_name = 'messager'

urlpatterns = [
    path('', views.MessageListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('<username>/', views.ConversationListView.as_view(), name='conversation_detail'),
]
