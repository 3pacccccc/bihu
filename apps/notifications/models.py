import uuid

from django.db import models

from users.models import User


class MessageQuerySet(models.query.QuerySet):

    def get_conversation(self, sender, recipient):
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('created_at')

    def get_most_recent_conversation(self, recipient):
        """
        获取最近一次私信互动的用户
        """
        try:
            qs_sent = self.filter(sender=recipient)
            qs_receive = self.filter(recipient=recipient)
            qs = qs_sent.union(qs_receive).latest('created_at')
            if qs.sender == recipient:
                return qs.recipient
            return qs.sender
        except self.model.DoesNotExist:
            return User.objects.get(username=recipient.username)

    def mark_as_read(self, sender, recipient):
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)


class Message(models.Model):
    """
    用户间私信
    """
    uuid_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    sender = models.ForeignKey(User, related_name='send_messages', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    recipient = models.ForeignKey(User, related_name='received_messages', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接收者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, db_index=True, verbose_name='是否未读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 没有updated_at，私信发送之后不能修改或撤回
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
