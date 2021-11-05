from django.urls import path

from .views import home as base_home, room as base_room
from .views import login_page as base_login_page
from .views import logout_user as base_logout
from .views import register_page as base_register_page
from .views import room_edit as base_room_edit
from .views import room_form as base_room_form
from .views import update_user as base_update_user
from .views import user_profile_page as base_user_profile_page

urlpatterns = [
    path('register/', base_register_page, name='base_register_page'),
    path('logout/', base_logout, name='base_logout'),
    path('login/', base_login_page, name='base_login_page'),
    path('', base_home, name="base_home"),
    path('room/<str:pk>/', base_room, name="base_room"),
    path('room_form/', base_room_form, name="base_room_form"),
    path('room_form/<str:pk>/', base_room_edit, name="base_room_edit"),
    path('profile/<str:pk>/', base_user_profile_page, name="base_user_profile_page"),
    path('update_user/', base_update_user, name="base_update_user"),
]
