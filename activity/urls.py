from django.urls import path
from .views import activity_page

urlpatterns = [
    path('', activity_page, name='activity_page')
]
