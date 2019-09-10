# __author__ = "MaRuiMin"

from django.test import RequestFactory
from test_plus import TestCase

from users.views import UserUpdateView


# RequestFactory可以不经过django的中间件，url路由，uwsgi等，直接测试view视图函数
class BaseUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()


class TestUserUpdateView(BaseUserTestCase):
    def setUp(self):
        super(TestUserUpdateView, self).setUp()
        self.view = UserUpdateView()
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)
