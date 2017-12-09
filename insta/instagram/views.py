from django.shortcuts import render,redirect


# Create your views here.

def index(request):

    title='instagram'
    return render(request, 'index.html', {"title": title})