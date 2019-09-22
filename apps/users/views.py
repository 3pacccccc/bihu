from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['moments_num'] = user.publisher.filter(reply=False).count()
        context['article_num'] = user.author.filter(status='P').count()
        # 在news下面的回复加上在article下面的回复, comment_comments是因为article使用的是django-comments\
        # 模块，在django-comments里面user的relatead_name是(%class)_comments
        context['comment_num'] = user.publisher.filter(
            reply=True).count() + user.comment_comments.all().count()
        context['question_num'] = user.q_author.all().count()
        context['answer_num'] = user.a_author.all().count()

        # 互动数
        tmp = set()
        # 我发送私信给了多少不同的用户
        sent_num = user.send_messages.all()
        for i in sent_num:
            tmp.add(i.recipient.username)
        # 我收到了多少私信
        recericed_num = user.received_messages.all()
        for r in recericed_num:
            tmp.add(r.sender.username)

        context['interaction_num'] = user.liked_news.all().count() + user.qa_voter.all().count() + context['comment_num'] + len(
            tmp)

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    用户只能更新自己的信息
    """
    fields = ['nickname', 'email', 'picture', 'introduction', 'job_title', 'location',
              'personal_url', 'weibo', 'zhihu', 'github', 'linkedin']
    model = User
    template_name = 'users/user_form.html'

    def get_success_url(self):
        # 更新成功后跳转到用户自己页面
        return reverse('users:detail', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
