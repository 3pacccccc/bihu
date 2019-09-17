# __author__ = "MaRuiMin"
from django.urls import path

# from articles.views import ArticleListView, CreateArticleView
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path('write-new-article/', views.CreateArticleView.as_view(), name='write_new'),
    path('drafts/', views.DraftListView.as_view(), name='drafts'),
    path('edit/<int:pk>/', views.EditArticleView.as_view(), name='edit_article'),
    path('<slug>/', views.DetailArticleView.as_view(), name='article'),
]
