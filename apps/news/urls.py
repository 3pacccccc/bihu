# __author__ = "MaRuiMin"
from django.urls import path

from news.views import NewsListView, post_news, NewsDeleteView, test, like

app_name = 'news'

urlpatterns = [
    path(r'', NewsListView.as_view(), name="list"),
    path('post-news/', post_news, name='post_news'),
    path('delete/<str:pk>', NewsDeleteView.as_view(), name='delete_news'),
    path('test/', test, name='test'),
    path('like/', like, name='like_post'),
]