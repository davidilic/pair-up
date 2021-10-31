from django.urls import path
from .views import home as base_home, room as base_room
from .views import room_form as base_room_form
from .views import logout_user as base_logout
from .views import room_edit as base_room_edit
from .views import room_delete as base_room_delete
from .views import login_page as base_login_page

urlpatterns = [
    path('logout/', base_logout, name='base_logout'),
    path('login/', base_login_page, name='base_login_page'),
    path('', base_home, name="base_home"),
    path('room/<str:pk>/', base_room, name="base_room"),
    path('room_form/', base_room_form, name="base_room_form"),
    path('room_form/<str:pk>/', base_room_edit, name="base_room_edit"),
    path('room_delete/<str:pk>/', base_room_delete, name="base_room_delete")
]
