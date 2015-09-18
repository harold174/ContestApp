from .models import Administrator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render

from .models import Video, Competitor
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import datetime
from contest.tasks import convertVideos


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
            return render(request, 'contest/dashboard.html')
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
    return render(request, 'contest/auth.html', context)


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

@login_required
def dashboard(request):
    return render(request, 'contest/dashboard.html')


def createContest(request):
    return render(request, 'contest/create.html')

def showContest(request):
    return render(request, 'contest/contest.html')

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
        convertVideos.delay(request.FILES['video'].name, video.id)
        return render(request, 'contest/upload.html')

    return render(request, 'contest/upload.html')