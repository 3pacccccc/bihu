from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django_comments.signals import comment_was_posted

from articles.forms import ArticleForm
from notifications.views import notification_handler
from utils.helper import AuthorRequireMixin
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


@method_decorator(cache_page(60 * 60), name='get')    # 将CreateArticleView GET方法返回的数据缓存
class CreateArticleView(LoginRequiredMixin, CreateView):
    """
    创建文章
    """
    model = Article
    message = "您的文章已经创建成功"  # Django框架中的消息机制
    form_class = ArticleForm
    template_name = 'articles/article_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateArticleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('articles:list')


class EditArticleView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    """
    编辑文章
    """
    model = Article
    message = "您的文章编辑成功"
    form_class = ArticleForm
    template_name = 'articles/article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditArticleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('articles:list')


class DetailArticleView(LoginRequiredMixin, DetailView):
    """
    文章详情
    """
    model = Article
    template_name = 'articles/article_detail.html'


class DraftListView(ArticleListView):
    """
    草稿箱列表
    """

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


def notify_comment(**kwargs):
    """
    文章有评论的时候通知作者
    :param kwargs:
    :return:
    """
    actor = kwargs['request'].user
    receiver = kwargs['comment'].content_object.user
    obj = kwargs['comment'].content_object
    notification_handler(actor, receiver, 'C', obj)


# 使用django_comments的信号机制,在文章有评论的时候出发信号量，执行notify_comment函数
comment_was_posted.connect(receiver=notify_comment)
