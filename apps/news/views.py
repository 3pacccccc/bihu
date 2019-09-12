import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from news.models import News
from utils.helper import ajax_require, AuthorRequireMixin


class NewsListView(LoginRequiredMixin, ListView):
    """
    网站首页动态
    """
    model = News
    # queryset = News.objects.all()
    paginate_by = 20  # 选择每页显示的数量
    # page_kwarg = 'p'   # 选择与前端交互的页码参数名,默认为page
    # context_object_name = 'news_list'   # 选择在前端模板语法中的名称{{news_list}}, 默认为(app_name)_list
    # ordering = 'create_at'
    template_name = 'news/news_list.html'

    # def get_ordering(self):
    #     """
    #     重写get_ordering可以实现更加复杂的排序
    #     :return:
    #     """
    #     pass

    def get_queryset(self):
        """
        重写get_queryset可以实现更加复杂的筛选过滤
        :return:
        """
        return News.objects.filter(reply=False)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """
    #     添加除了context_object_name以外其他的上下文
    #     :param object_list:
    #     :param kwargs:
    #     :return:
    #     """
    #     context = super(NewsListView, self).get_context_data()
    #     context['views'] = 100
    #     return context


@login_required
@ajax_require
@require_http_methods(['POST'])
def post_news(request):
    # 用户发表文章
    post = request.POST.get('post', '').strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
    else:
        return HttpResponseBadRequest("发表内容不能为空")

    return render(request, 'news/news_single.html', {'news': posted})


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    slug_url_kwarg = "slug"  # 通过url传入要删除的对象主键ID，默认是slug
    # pk_url_kwarg = 'pk'  # 在数据库中根据某个字段进行查找删除
    success_url = reverse_lazy('news:list')


def like(request):
    news_id = request.POST.get('news')

    news_obj = News.objects.get(pk=news_id)
    if request.user in news_obj.liked.all():
        news_obj.liked.remove(request.user)
    else:
        news_obj.liked.add(request.user)
    # 获取点赞数量
    news_like_count = news_obj.liked.count()
    # 获取点赞人员列表
    return JsonResponse({'likes': news_like_count})


def test(request):
    time.sleep(10)
    return HttpResponse("ok", content_type='application/json')