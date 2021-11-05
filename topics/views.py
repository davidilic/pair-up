from django.shortcuts import render

from base.models import Topic, Room


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    rooms = Room.objects.all()

    context = {
        'topics': topics,
        'rooms': rooms
    }

    return render(request, 'topics.html', context)
