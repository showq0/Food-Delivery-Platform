"""
ASGI config for food_delivery_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import customer_support_chat.routing
import order_tracking.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_platform.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            order_tracking.routing.websocket_urlpatterns + customer_support_chat.routing.websocket_urlpatterns

        )
    ),
})
