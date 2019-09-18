from django.test import Client
from django.urls import reverse
from test_plus import TestCase

from news.models import News


class NewsViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user('user01')
        self.other_user = self.make_user('user02')
        self.client = Client()
        self.other_client = Client()
        self.client.login(username='user01', password='password')
        self.other_client.login(username='user02', password='password')
        self.first_news = News.objects.create(
            user=self.user,
            content='第一条动态'
        )
        self.second_news = News.objects.create(
            user=self.user,
            content='第二条动态'
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content='第一条动态的评论',
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        """
        测试动态列表页功能
        :return:
        """
        response = self.client.get(reverse('news:list'))
        assert response.status_code == 200
        assert self.first_news in response.context['news_list']
        assert self.second_news in response.context['news_list']
        assert self.third_news not in response.context['news_list']

    def test_delete_news(self):
        """
        删除动态
        :return:
        """
        response = self.client.post(reverse('news:delete_news', kwargs=self.first_news.id))
        # 删除第二条动态，会将评论也删除
        assert response.status_code == 302
        assert News.objects.count() == 1


