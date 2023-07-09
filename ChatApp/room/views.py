from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RoomForm, deleteRoom, enterRoom
from .models import Room

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})


def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            util = form.cleaned_data
            name = util['name']
            slug = util['slug']
            password = util['psswd']
            Room.objects.create(name=name, slug=slug, created_by=request.user ,psswd=password)
            return redirect('rooms')
    else:
        form = RoomForm()
    return render(request, 'room/create.html', {'form': form})


@login_required
def enter_room(request, slug):
    room = Room.objects.get(slug=slug)
    if room.created_by == request.user:
        return render(request, 'room/room.html', {'room': room})
    if request.method == 'POST':
        form = enterRoom(request.POST)
        if form.is_valid():
            util = form.cleaned_data
            password = util['psswd']
            if room.psswd == password:
                return render(request, 'room/room.html', {'room': room})
            else:
                error_message = 'Incorrect password. Please try again.'
                return render(request, 'room/room.html', {'room': room, 'error_message': error_message})

    else:
        return render(request, 'room/enter.html', {'room': room})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'room/room.html', {'room': room})


@login_required
def delete_room(request, slug):
    room = Room.objects.get(slug=slug)
    if request.method == 'POST':
        form = deleteRoom(request.POST)
        if form.is_valid():
            util = form.cleaned_data
            password = util['psswd']
            if room.psswd == password:
                room.delete()
                return redirect('rooms')
            else:
                error_message = 'Incorrect password. Please try again.'
                return render(request, 'room/delete.html', {'room': room, 'error_message': error_message})
    else:
        form = deleteRoom()
    return render(request, 'room/delete.html', {'form': form, 'room': room})