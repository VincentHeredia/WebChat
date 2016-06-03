from django.shortcuts import render
from django.template import loader

# Create your views here.


def chatRoom(request):
    return render(request, 'chat/chatRoom.html')