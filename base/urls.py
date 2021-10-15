from django.urls import path
from .views import home as base_home, room as base_room

urlpatterns = [
    path('', base_home, name="base_home"),
    path('room/<str:pk>/', base_room, name="base_room")
]
