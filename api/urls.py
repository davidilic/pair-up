from django.urls import path

from .views import get_room as api_get_room
from .views import get_rooms as api_get_rooms
from .views import get_routes as api_get_routes

urlpatterns = [
    path('', api_get_routes, name='api_get_routes'),

    path('rooms/', api_get_rooms, name='api_get_rooms'),
    path('rooms/<str:pk>', api_get_room, name='api_get_room'),
]
