# __author__ = "MaRuiMin"
from django.urls import path

from news.views import NewsListView

app_name = 'news'

urlpatterns = [
    path(r'', NewsListView.as_view(), name="list"),

]