from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Create your views here.
def index(request):
    context = {'var': 'Hello Contest!!'}
    return render(request, 'contest/index.html', context)


def auth(request):
    context = {'var': 'Auth!!'}
    return render(request, 'contest/auth.html', context)


def login(request):
    context = {'var': 'Login!!'}
    return render(request, 'contest/login.html', context)


def register(request):
    context = {'var': 'Register!!'}
    return render(request, 'contest/register.html', context)