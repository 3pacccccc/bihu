from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView

from notifications.models import Notifications


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """
    未读通知列表
    """
    model = Notifications
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notification_list'

    def get_queryset(self):
        return Notifications.objects.filter(recipient=self.request.user, unread=True)

    
@login_required
def mark_all_as_read(request):
    """
    所有通知标记为已读
    :param request:
    :return:
    """
    notifications_obj = Notifications.objects.filter(recipient=request.user)
    notifications_obj.update(unread=False)
    _next = request.GET.get('next')
    messages.add_message(request, messages.SUCCESS, "用户{0}的所有通知标为已读".format(request.user.username))
    if _next:
        return redirect(_next)
    return redirect("notifications:unread")


@login_required
def mark_as_read(request, slug):
    notification = get_object_or_404(Notifications, slug=slug)
    notification.unread = False
    notification.save()
    _next = request.GET.get('next')

    messages.add_message(request, messages.SUCCESS, "通知{0}标为已读".format(notification))
    if _next:
        return redirect(_next)
    return redirect("notifications:unread")


@login_required
def get_latest_notifications(request):
    notifications = Notifications.objects.filter(recipient=request.user, unread=True)[:5]
    return render(request, 'notifications/most_recent.html', {'notifications': notifications})


def notification_handler(actor, recipient, verb, action_object, **kwargs):
    """
    消息通知处理器
    :param actor:                   request.user对象，通知的执行者
    :param recipient:             User对象，通知的接收者
    :param verb:                    str  通知的动作
    :param action_object:      Instance  动作对象的实例
    :param kwargs:                key, id_value等
    :return:
    """
    if actor != recipient:
        key = kwargs.get('key', 'notification')
        id_value = kwargs.get('id_value', None)
        # 记录通知内容
        Notifications.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=action_object
        )
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            "key": key,
            'actor_name': actor.username,
            'id_value': id_value,
            'recipient': recipient.username
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
