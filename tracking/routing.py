# routing.py
from django.urls import path
from .consumers import DriverLocationConsumer

websocket_urlpatterns = [
    path('ws/track-driver/<int:driver_id>/', DriverLocationConsumer.as_asgi()),
]
