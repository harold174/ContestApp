from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    context = {'var': 'hii'}
    return render(request, 'contest/index.html', context)