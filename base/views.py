from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User, Message
from .forms import roomForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import userForm as UserForm


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('base_home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base_home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {'page': page}
    return render(request, 'login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('base_home')


def register_page(request):
    form = UserCreationForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('base_home')
        else:
            messages.error(request, "An error occurred during registration.")

    return render(request, 'login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
    )

    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]

    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': recent_messages,
    }

    return render(request, 'home.html', context)


def room(request, pk):
    rooms = Room.objects.all()
    room_for_html = rooms.get(id=pk)

    room_messages = room_for_html.message_set.all().order_by('-created')
    participants = room_for_html.participants.all()

    if request.method == "POST":
        new_message = Message.objects.create(
            user=request.user,
            room=room_for_html,
            body=request.POST.get('body')
        )
        room_for_html.participants.add(request.user)
        return redirect('base_room', pk=pk)

    context = {
        'room': room_for_html,
        'room_messages': room_messages,
        'participants': participants
    }

    return render(request, 'room.html', context=context)


def user_profile_page(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'recent_messages': recent_messages,
        'topics': topics
    }

    return render(request, 'profile.html', context)


@login_required(login_url='base_login_page')
def room_form(request):
    form = roomForm()
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


@login_required(login_url='base_login_page')
def room_edit(request, pk):
    room_ = Room.objects.get(id=pk)
    form = roomForm(instance=room_)
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
def room_delete(request, pk):
    room_instance = Room.objects.get(id=pk)
    form = roomForm(instance=room_instance)

    if request.user != room_instance.host:
        return HttpResponse("You are not allowed to do that.")

    if request.method == 'POST':
        room_instance.delete()
        return redirect('base_home')

    return render(request, 'delete.html', context={'form': form})


@login_required(login_url='base_login_page')
def message_delete(request, pk):
    message_instance = Message.objects.get(id=pk)

    if request.user != message_instance.user:
        return HttpResponse("You are not allowed to do that.")

    if request.method == 'POST':
        message_instance.delete()
        return redirect('base_home')

    return render(request, 'delete.html', context={'obj': message_instance})


@login_required(login_url='base_login_page')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base_user_profile_page', pk=user.id)

    context = {
        'form': form
    }

    return render(request, 'update_user.html', context)

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics':topics}

    return render(request, 'topics.html', context)

def activity_page(request):
    room_messages = Message.objects.all()

    context = {'room_messages': room_messages}

    return render(request, 'activity.html', context)
