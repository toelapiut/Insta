from django.shortcuts import render,redirect


# Create your views here.

def index(request):

    title='Hello world'
    return render(request, 'index.html', {"title": title})