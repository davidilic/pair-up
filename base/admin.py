from django.contrib import admin

from .models import User, Room, Message, Topic

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Room)
