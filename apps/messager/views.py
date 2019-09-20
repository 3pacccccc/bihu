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
