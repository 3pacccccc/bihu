from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from articles.forms import ArticleForm
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    paginate_by = 10
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


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




