from django.urls import path
from .consumers import ColorConsumer

websocket_urlpatterns =[
    path("ws/color/<str:room_id>/", ColorConsumer.as_asgi())
]