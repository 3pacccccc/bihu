from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
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


@login_required
@ajax_require
@require_http_methods(['POST'])
def like(request):
    news_id = request.POST.get('news')
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)
    return JsonResponse({"likes": news.count_likers()})
    #
    # news_obj = News.objects.get(pk=news_id)
    # if request.user in news_obj.liked.all():
    #     news_obj.liked.remove(request.user)
    # else:
    #     news_obj.liked.add(request.user)
    # # 获取点赞数量
    # news_like_count = news_obj.liked.count()
    # # 获取点赞人员列表
    # return JsonResponse({'likes': news_like_count})


@login_required
@ajax_require
@require_http_methods(['GET'])
def get_thread(request):
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    # render_to_string()表示加载模板，填充数据，返回字符串
    heart_auth = request.user in news.get_likers()
    news_html = render_to_string("news/news_single.html", {"news": news, 'heart_auth': heart_auth})  # 没有评论的时候
    threads = News.objects.filter(parent=news_id).all()
    # thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})  # 有评论的时候
    username = request.user.username
    user = request.user
    thread_html = render_to_string("news/news_thread.html", {"thread": threads, "user": user, "username": username})  # 有评论的时候
    return JsonResponse({
        'uuid': news_id,
        'news': news_html,
        'thread': thread_html
    })


@login_required
@ajax_require
@require_http_methods('[POST')
def post_reply(request):
    reply = request.POST.get('reply', '').strip()
    news_id = request.POST.get('parent', '')
    news_obj = News.objects.get(pk=news_id)
    if reply:
        news_obj.reply_this(user=request.user, text=reply)
        return JsonResponse({'comments': news_obj.comment_count()})

    else:
        return HttpResponseBadRequest("发表内容不能为空")


@login_required
@ajax_require
@require_http_methods(["POST"])
def update_interactions(request):
    # 更新评论以及点赞数
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    data = {'likes': news.count_likers(), 'comments': news.comment_count()}
    return JsonResponse(data)
