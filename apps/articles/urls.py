# __author__ = "MaRuiMin"
from django.urls import path

from articles.views import ArticleListView, CreateArticleView

app_name = 'articles'

urlpatterns = [

    path('', ArticleListView.as_view(), name='list'),
    path('write-new-article/', CreateArticleView.as_view(), name='write_new'),
]
