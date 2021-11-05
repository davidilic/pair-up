from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.forms import RoomForm
from base.models import Room, Topic, Message


@login_required(login_url='base_login_page')
def room_edit(request, pk):
    room_ = Room.objects.get(id=pk)
    form = RoomForm(instance=room_)
    topics = Topic.objects.all()

    if request.user != room_.host:
        return HttpResponse("You are not allowed to do that.")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room_.name = request.POST.get('name')
        room_.topic = topic
        room_.description = request.POST.get('description')
        room_.save()

        return redirect('base_home')

    context = {
        'form': form,
        'topics': topics,
        'room': room_
    }

    return render(request, 'room_form.html', context)


@login_required(login_url='base_login_page')
def room_create(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('base_home')

    context = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'room_form.html', context)


def room(request, pk):
    rooms = Room.objects.all()
    room_for_html = rooms.get(id=pk)

    room_messages = room_for_html.message_set.all().order_by('created')
    participants = room_for_html.participants.all()

    if request.method == "POST":

        message_body = request.POST.get('body')

        if len(message_body) > 4000:
            messages.error(request, "Message too long.")
            return redirect('rooms_room', pk=pk)

        Message.objects.create(
            user=request.user,
            room=room_for_html,
            body=message_body
        )

        room_for_html.participants.add(request.user)
        return redirect('rooms_room', pk=pk)

    context = {
        'room': room_for_html,
        'room_messages': room_messages,
        'participants': participants
    }

    return render(request, 'room.html', context=context)
