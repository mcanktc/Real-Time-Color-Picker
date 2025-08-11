from channels.routing import URLRouter
from cpickerapp.routing import websocket_urlpatterns

URLRouter(websocket_urlpatterns)