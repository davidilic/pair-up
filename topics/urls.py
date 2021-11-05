from django.urls import path

from .views import topics_page

urlpatterns = [
    path('', topics_page, name='topics_page')
]

