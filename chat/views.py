from django.shortcuts import render, get_object_or_404
from django.views import generic

# Create your views here.


class IndexView(generic.ListView):
	template_name = "chat/index.html"