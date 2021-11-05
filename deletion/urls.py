from django.urls import path
from .views import delete_room as deletion_room
from .views import delete_message as deletion_message

urlpatterns = [
    path('room/<str:pk>/', deletion_room, name='deletion_room'),
    path('message/<str:pk>/', deletion_message, name='deletion_message'),
]

