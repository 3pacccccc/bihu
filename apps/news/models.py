import uuid

from django.db import models

from users.models import User


class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='publisher',
                             verbose_name='用户')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='thread',
                               verbose_name='自关联')
    content = models.TextField(verbose_name='动态内容')
    liked = models.ManyToManyField(User, related_name='liked_news', verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

    def switch_like(self, user):
        """
        点赞或者取消赞
        :param user: 当前用户
        :return:
        """
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

    def get_parent(self):
        """
        返回自关联中的上级记录或者本身
        :return:
        """
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        """
        回复首页的动态
        :param user: 当前登陆的用户
        :param text: 回复的内容
        :return:
        """
        parent = self.get_parent()
        reply_news = News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )
