from test_plus import TestCase


class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user(username="xiaoma")

    def test___str__(self):
        self.assertEqual(self.user.__str__(), "xiaoma")

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/xiaoma/')

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == 'xiaoma'
        self.user.nickname = "mage"
        assert self.user.get_profile_name() == 'mage'
