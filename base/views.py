from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User
from .forms import roomForm
from django.shortcuts import redirect
from django.db.models import Q


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('base_home')
        else:
            messages.error(request,"Username or password does not exist")


    context = {}
    return render(request, 'login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('base_home')


def home(request):

    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
        )

    room_count = rooms.count()

    topics = Topic.objects.all()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }

    return render(request, 'home.html', context)


def room(request, pk):
    rooms = Room.objects.all()
    room_for_html = rooms.get(id=pk)
    return render(request, 'room.html', context={'room': room_for_html})


def room_form(request):
    form = roomForm()

    if request.method == 'POST':
        form = roomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base_home')
    context = {'form': form}
    return render(request, 'room_form.html', context)


def room_edit(request, pk):
    room = Room.objects.get(id=pk)
    form = roomForm(instance=room)

    if request.method == 'POST':
        form = roomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base_home')

    context = {'form': form}

    return render(request, 'room_form.html', context)


def room_delete(request, pk):
    room_instance = Room.objects.get(id=pk)
    form = roomForm(instance=room_instance)

    if request.method == 'POST':
        room_instance.delete()
        return redirect('base_home')

    return render(request, 'room_delete.html', context={'form': form})
