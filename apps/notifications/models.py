import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models
from slugify import slugify

from users.models import User


class NotificationQuerySet(models.query.QuerySet):

    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient):
        """
        全部标记为已读
        :return:
        """
        notification_obj = self.filter(recipient=recipient)
        return notification_obj.update(unread=False)

    def mark_all_as_unread(self, recipient):
        notification_obj = self.filter(recipient=recipient)
        return notification_obj.update(unread=True)

    def get_most_recent(self, recipient):
        notification_obj = self.filter(recipient=recipient, unread=True)[:5]
        return notification_obj

    def serialize_latest_notifications(self, recipient):
        qs = self.get_most_recent(recipient)
        notification_dic = serializers.serialize('json', qs)
        return notification_dic


class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('L', '赞了'), ('C', '评论了'), ('F', '收藏了'), ('A', '回答了'), ('W', '接受了回答'), ('R', '回复了'), ('I', '登录'), ('O', '退出'),
    )
    uuid_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    actor = models.ForeignKey(User, related_name='notify_actor', on_delete=models.CASCADE, verbose_name='触发者')
    recipient = models.ForeignKey(User, related_name='notifications', null=True, blank=True, on_delete=models.CASCADE,
                                  verbose_name='接收者')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='未读')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPES, verbose_name='通知类别')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = NotificationQuerySet.as_manager()

    # 使Notifications变成通用外键
    object_id = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, related_name='notify_action_object', blank=True, null=True,
                                     on_delete=models.CASCADE)
    action_object = GenericForeignKey()  # 或GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        if self.action_object:
            return f'{self.actor} {self.get_verb_display()} {self.action_object}'
        return f'{self.actor} {self.get_verb_display()}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.recipient} {self.uuid_id} {self.verb}')
        super(Notifications, self).save(*args, **kwargs)

    def get_icon(self):
        """根据通知类别，返回通知下拉菜单中的样式"""
        if self.verb == 'C' or self.verb == 'A':
            return 'fa-comment'

        elif self.verb == 'L':
            return 'fa-heart'

        elif self.verb == 'F':
            return 'fa-star'

        elif self.verb == 'W':
            return 'fa-check-circle'

        elif self.verb == 'R':
            return 'fa-reply'

        elif self.verb == 'I' or self.verb == 'U' or self.verb == 'O':
            return 'fa-users'

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()
