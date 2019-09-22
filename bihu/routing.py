# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from messager.consumers import MessagesConsumer
from notifications.consumers import NotificationsConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/notifications/', NotificationsConsumer),
                path('ws/<username>/', MessagesConsumer),
            ])
        )
    )
})

"""
OriginValidator或AllowedHostsOriginValidator可以防止通过WebSocket进行CSRF攻击
OriginValidator需要手动添加允许访问的源站，如：

from channels.security.websocket import OriginValidator
application = ProtocolTypeRouter({

    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                ...
            ])
        ),
        [".imooc.com", "http://.imooc.com:80", "http://muke.site.com"],
    ),
})

而使用AllowedHostsOriginValidator，允许访问的源站与settings.py文件中的ALLOWED_HOSTS相同
AuthMiddleware用于WebSocket认证，集成了CookieMiddleware, SessionMiddleware, AuthMiddleware, 兼容Django的认证系统
"""