from django.shortcuts import render
from django.template import loader

# Create your views here.


def index(request):
    template = loader.get_template('chat/index.html')
    return render(request, 'chat/index.html')