# __author__ = "MaRuiMin"
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View


def ajax_require(f):
    # 验证是否是AJAX请求
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是AJAX请求")
        else:
            return f(request, *args, **kwargs)

    return wrap


class AuthorRequireMixin(View):
    """
    验证是否为原作者，用于状态删除、文章编辑；
    个人中心模块中更新信息不要验证是否为原作者，因为UserUpdateView返回的是当前登录用户的form
    """
    def dispatch(self, request, *args, **kwargs):
        # 状态和文章实例有user属性
        if self.get_object().user.username != self.request.user.username:
            return PermissionDenied

        return super(AuthorRequireMixin, self).dispatch(request, *args, **kwargs)
