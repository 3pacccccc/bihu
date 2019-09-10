# __author__ = "MaRuiMin"

from django.urls import reverse, resolve
from test_plus import TestCase


class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user(username="xiaoma")

    def test_update_resolve(self):
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), '/users/update/')

    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/{0}/'.format(self.user.username)).view_name, 'users:detail')

    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={'username': self.user.username}),
                         '/users/{0}/'.format(self.user.username))
