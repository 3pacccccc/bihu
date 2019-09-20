# __author__ = "MaRuiMin"
from django.urls import path

from users.views import UserDetailView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path(r'update/', UserUpdateView.as_view(), name="update"),
    path('<str:username>/', UserDetailView.as_view(), name="detail")
]