from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from news.models import News


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
