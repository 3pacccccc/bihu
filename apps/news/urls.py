# __author__ = "MaRuiMin"
from django.urls import path

from news.views import NewsListView, post_news, NewsDeleteView, like, get_thread, post_reply

app_name = 'news'

urlpatterns = [
    path(r'', NewsListView.as_view(), name="list"),
    path('post-news/', post_news, name='post_news'),
    path('delete/<str:pk>', NewsDeleteView.as_view(), name='delete_news'),
    path('like/', like, name='like_post'),
    path('get-thread/', get_thread, name='get_thread'),
    path('post-comment/', post_reply, name='post_comments'),
]