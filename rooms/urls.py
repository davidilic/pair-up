from django.urls import path

from .views import room as rooms_room
from .views import room_create as rooms_room_create
from .views import room_edit as rooms_room_edit

urlpatterns = [
    path('room/<str:pk>/', rooms_room, name='rooms_room'),
    path('room_create/', rooms_room_create, name='rooms_room_create'),
    path('room_edit/<str:pk>/', rooms_room_edit, name='rooms_room_edit'),
]