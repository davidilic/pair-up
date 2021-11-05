from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.forms import RoomForm
from base.models import Room, Message


@login_required(login_url='base_login_page')
def delete_room(request, pk):
    room_instance = Room.objects.get(id=pk)
    form = RoomForm(instance=room_instance)

    if request.user != room_instance.host:
        return HttpResponse("You are not allowed to do that.")

    if request.method == 'POST':
        room_instance.delete()
        return redirect('base_home')

    context = {
        'form': form,
        'obj': room_instance
    }

    return render(request, 'delete.html', context)


@login_required(login_url='base_login_page')
def delete_message(request, pk):
    message_instance = Message.objects.get(id=pk)

    if request.user != message_instance.user:
        return HttpResponse("You are not allowed to do that.")

    if request.method == 'POST':
        room_id = message_instance.room_id
        message_instance.delete()
        return redirect('rooms_room', room_id)

    return render(request, '../templates/delete.html', context={'obj': message_instance})
