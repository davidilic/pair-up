from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RoomForm, NewUserCreationForm, UserForm
from .models import Room, Topic, User, Message


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('base_home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('base_home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {'page': page}
    return render(request, 'user_login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('base_home')


def register_page(request):
    form = NewUserCreationForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base_home')
        else:
            messages.error(request, "An error occurred during registration.")

    return render(request, 'user_login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
    )

    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]

    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': recent_messages,
    }

    return render(request, 'home.html', context)


def user_profile_page(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_messages = user.message_set.all()
    topics = Topic.objects.filter(room__host_id=user.id)

    context = {
        'user': user,
        'rooms': rooms,
        'recent_messages': recent_messages,
        'topics': topics
    }

    return render(request, 'user_profile.html', context)


@login_required(login_url='base_login_page')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base_user_profile_page', pk=user.id)

    context = {
        'form': form
    }

    return render(request, 'user_update.html', context)
