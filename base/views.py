from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id': 1, 'name': 'lets learn django'},
    {'id': 2, 'name': 'lets learn java'},
    {'id': 3, 'name': 'lets learn c#'},
    {'id': 4, 'name': 'lets learn web dev'}
]


def home(request):
    return render(request, 'home.html', context={'rooms': rooms})


def room(request, pk):
    room = None
    for i in rooms:
        if(i['id'] == int(pk)):
            room = i

    return render(request, 'room.html', context={'room':room})
