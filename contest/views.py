from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Administrator, Contest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from .models import Video, Competitor
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.files import File
import datetime
import re

# Create your views here.
def index(request):
    context = {'var': 'Hello Contest!!'}
    return render(request, 'contest/index.html', context)


def auth(request):
    context = {'var': 'Auth!!'}
    return render(request, 'contest/auth.html', context)


def login(request):
    #Capture parameter
    error=""
    username = request.POST['username']
    password=request.POST['password']
    #Autenticate
    user = authenticate(username=username, password=password)
    if user is not None:
        #the password verified for the user
        if user.is_active:
            auth_login(request, user)
            print("User is valid, active and authenticated")
            return redirect('/contest/dashboard', request)
        else:
            error="The password is valid, but the account has been disabled!"
    else:
        # the authentication system was unable to verify the username and password
        error="The username and password were incorrect."

    context = {'error_auth': error}
    return render(request, 'contest/auth.html', context)


def logoutView(request):
    logout(request)
    context = {'var': 'Logout!!'}
    return redirect('/contest')


def register(request):
    error=""
    #Capture parameter
    email = request.POST['email']
    username = request.POST['username']
    firstname= request.POST['firstname']
    lastname= request.POST['firstname']
    password=request.POST['password']
    password2=request.POST['password2']
    if(password!=password2):
        error="Passwords don't match them"
    else:
        #Saves user
        user=User.objects.create_user(first_name=firstname, last_name=lastname, password=password, email=email, username=username)
        user.save()
        #Saves administrator
        admin = Administrator(first_name=firstname, last_name=lastname, password=password, email=email, username=username, user=user)
        admin.save()
    #Return page
    context = {'error_reg': error}
    return render(request, 'contest/auth.html', context)

@login_required(login_url='/contest/auth/')
def dashboard(request):
    admin = Administrator.objects.get(user=request.user)
    contests = Contest.objects.all().filter(owner_id = admin.id)[:50]
    context = {'username': request.user.username, 'contests': contests, 'page':contests.count()}
    return render(request, 'contest/dashboard.html', context)


@login_required(login_url='/contest/auth/')
def createContest(request):
    context = {'username': request.user.username}
    return render(request, 'contest/create.html', context)

@login_required(login_url='/contest/auth/')
def showContest(request):
    context = {'username': request.user.username}
    return render(request, 'contest/contest.html', context)

@login_required(login_url='/contest/auth/')
def saveContest(request):

    try:
        name = request.POST['name']
        url = request.POST['url']
        start = request.POST['start']
        end = request.POST['end']
        prize = request.POST['prize']
        image = request.FILES['image']
        if name and url and start and end and prize :
            matInit = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', start)
            matEnd = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', end)
            if matInit is None or matEnd is None:
                context = {'message':'Dates must have the format yyy/mm/dd'}
                return render(request,'contest/create.html', context)

            valUrl = re.match('[a-zA-Z_0-9]*',url)
            if valUrl is None:
                context = {'message':'Url contest must have only numbers, uppercase letters, lowercase letters, or _'}
                return render(request,'contest/create.html', context)

            init = datetime.datetime.strptime(start, "%Y/%m/%d")
            finish = datetime.datetime.strptime(end, "%Y/%m/%d")
            contest = Contest(name=name,image=image, url=url, start_date=init, end_date = finish, created_date=datetime.datetime.now(),
                              prize = prize, owner=Administrator.objects.get(user=request.user))
            contest.save()
            return redirect('/contest/dashboard')
        else:
            context={'message':'All fields are mandatory'}
            return render(request,'contest/create.html', context)

    except ValueError:
        context = {'message':'Exception in validation of fields '}
        return render(request,'contest/create.html', context)


def contestPublic(request, id):
    return render(request, 'contest/contest_public.html')



def upload(request, id):
    if request.method == 'POST':
        #create competitor
        competitor = Competitor(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
        competitor.save()
        video = Video(message=request.POST['message'], path_original=request.FILES['video'], owner=competitor,
                      status=1, created_date=datetime.datetime.now())
        video.save()
        return render(request, 'contest/upload.html')

    return render(request, 'contest/upload.html')