from django.shortcuts import render

from base.models import Message


def activity_page(request):
    room_messages = Message.objects.all()

    context = {'room_messages': room_messages}

    return render(request, 'activity.html', context)
