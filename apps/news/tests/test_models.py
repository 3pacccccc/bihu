from test_plus import TestCase

from news.models import News


class NewsTestModels(TestCase):
    def setUp(self):
        self.user1 = self.make_user("user1")
        self.user2 = self.make_user("user2")
        self.news1 = News.objects.create(
            user=self.user1,
            parent=None,
            content="news1"
        )
        self.news2 = News.objects.create(
            user=self.user2,
            parent=None,
            content="news2"
        )
        self.news3 = News.objects.create(
            user=self.user2,
            parent=self.news1,
            content="comment on news1 by user2"
        )
        self.news4 = News.objects.create(
            user=self.user1,
            parent=self.news2,
            content='comment on news2 by user1'
        )

    def test_switch_like(self):
        self.news1.switch_like(self.user2)
        self.assertEqual(self.news1.liked.count(), 1)
        self.news1.switch_like(self.user2)
        self.assertEqual(self.news1.liked.count(), 2)

    def test_get_parent(self):
        self.assertEqual(self.news3.get_parent(), self.news1)
        self.assertEqual(self.news4.get_parent(), self.news2)
        self.assertEqual(self.news1.get_parent(), self.news1)
        self.assertEqual(self.news2.get_parent(), self.news2)

    def test_reply_this(self):
        self.assertEqual(self.news1.reply_this(self.user2, "comment on news1 by user2"), self.news3)
        self.assertEqual(self.news2.reply_this(self.user1, "comment on news2 by user1"), self.news4)


    def test_count_likers(self):
        self.news1.switch_like(self.user1)
        self.news1.switch_like(self.user2)
        self.assertEqual(self.news1.count_likers(), 2)

    def test_comment_count(self):
        self.assertEqual(self.news1.comment_count(), 1)
        self.assertEqual(self.news2.comment_count(), 1)
        self.assertEqual(self.news3.comment_count(), 1)
        self.assertEqual(self.news4.comment_count(), 1)

    def test_get_thread(self):
        self.assertEqual(self.news1.get_thread(), [self.news1, self.news3])
        self.assertEqual(self.news2.get_thread(), [self.news2, self.news4])

    def test_delete_auth(self):
        self.assertEqual(self.news1.delete_auth(self.user1), True)
        self.assertEqual(self.news1.delete_auth(self.user2), False)
        self.assertEqual(self.news2.delete_auth(self.user1), False)
        self.assertEqual(self.news2.delete_auth(self.user2), True)
        self.assertEqual(self.news3.delete_auth(self.user1), False)
        self.assertEqual(self.news2.delete_auth(self.user2), True)
        self.assertEqual(self.news4.delete_auth(self.user1), True)
        self.assertEqual(self.news4.delete_auth(self.user2), False)
