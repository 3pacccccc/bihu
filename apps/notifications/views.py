from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from messager.models import Message
from users.models import User
from utils.helper import ajax_require


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messager/message_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(*args, **kwargs)
        context['users_list'] = User.objects.filter(is_active=True).exclude(username=self.request.user.username).order_by('-last_login')
        last_conversation = Message.objects.get_most_recent_conversation(self.request.user)
        context['active'] = last_conversation.username
        return context

    def get_queryset(self):
        """
        最近一次私信互动的内容
        """
        active_user = Message.objects.get_most_recent_conversation(self.request.user)
        return Message.objects.get_conversation(active_user, self.request.user)


class ConversationListView(MessageListView):
    """
    与指定用户的私信内容
    """

    def get_context_data(self, *args, **kwargs):
        context = super(ConversationListView, self).get_context_data(*args, **kwargs)
        context['active'] = self.kwargs['username']
        return context

    def get_queryset(self):
        active_user = get_object_or_404(User, username=self.kwargs['username'])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_require
@require_http_methods(["POST"])
def send_message(request):
    """
    发送消息，ajax请求
    :param request:
    :return:
    """
    sender = request.user
    recipient_username = request.POST.get('to', '')
    recipient = get_object_or_404(User, username=recipient_username)
    message = request.POST.get('message')
    # 内容不能为空且不是发送给自己
    if len(message.strip()) != 0 and sender != recipient:
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',   # 表示将消息传递给当前channel_layer的receive函数处理
            'key': 'message',
            'message_id': str(msg.uuid_id),
            'sender': sender.username,
            'recipient': recipient.username
        }
        async_to_sync(channel_layer.group_send)(recipient.username, payload)

        return render(request, 'messager/single_message.html', {'message': msg})

    return HttpResponse("发送失败", content_type='application/json')

