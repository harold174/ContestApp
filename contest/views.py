import datetime
import re

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Administrator, Contest
from .models import Video, Competitor
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
    allContest = Contest.objects.all().filter(owner_id = admin.id, enable = True).order_by('-created_date')
    paginator = Paginator(allContest, 50) # Show 50 contacts per page
    page = request.GET.get('page')
    try:
        contests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contests = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contests = paginator.page(paginator.num_pages)

    context = {'username': request.user.username, 'contests': contests, 'pages': paginator.page_range}
    return render(request, 'contest/dashboard.html', context)


@login_required(login_url='/contest/auth/')
def createContest(request):
    context = {'username': request.user.username}
    return render(request, 'contest/create.html', context)

@login_required(login_url='/contest/auth/')
def showContest(request, url):
    admin = Administrator.objects.get(user=request.user)
    contest = Contest.objects.get(owner_id = admin.id, url = url)
    if contest and contest.enable:
        allVideos = Video.objects.all().filter(contest = contest).order_by('-created_date')
        paginator = Paginator(allVideos, 50) # Show 50 contacts per page
        page = request.GET.get('page')
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            videos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            videos = paginator.page(paginator.num_pages)
        context = {'username': request.user.username, 'contest':contest,'videos': videos, 'pages': paginator.page_range}
    else:
        context = {'message':'The contest is not available'}
    return render(request, 'contest/contest.html', context)

@login_required(login_url='/contest/auth/')
def editContest(request, id):
    admin = Administrator.objects.get(user=request.user)
    contest = Contest.objects.get(owner_id = admin.id, id = id)
    if contest and contest.enable:
        context = {'username': request.user.username, 'contest':contest}
        return render(request, 'contest/create.html', context)
    else:
        context = {'username': request.user.username, 'message':'The contest is not available'}
        return render(request, 'contest/contest.html', context)

@login_required(login_url='/contest/auth/')
def deleteContest(request, id):
    admin = Administrator.objects.get(user=request.user)
    contest = Contest.objects.get(owner_id = admin.id, id = id)
    if contest and contest.enable:
        contest.enable=False
        contest.save()
    return redirect('/contest/dashboard/')


@login_required(login_url='/contest/auth/')
def saveCreateContest(request):

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
                context = {'username': request.user.username,'message':'Dates must have the format yyy/mm/dd'}
                return render(request,'contest/create.html', context)

            valUrl = re.match('[a-zA-Z_0-9]*',url)
            if valUrl is None:
                context = {'username': request.user.username,'message':'Url contest must have only numbers, uppercase letters, lowercase letters, or _'}
                return render(request,'contest/create.html', context)

            init = datetime.datetime.strptime(start, "%Y/%m/%d")
            finish = datetime.datetime.strptime(end, "%Y/%m/%d")
            contest = Contest(name=name,image=image, url=url, start_date=init, end_date = finish, created_date=datetime.datetime.now(),
                              prize = prize, owner=Administrator.objects.get(user=request.user))
            contest.save()
            return redirect('/contest/dashboard')
        else:
            context={'username': request.user.username,'message':'All fields are mandatory'}
            return render(request,'contest/create.html', context)

    except :
        context = {'username': request.user.username,'message':'Exception in validation of fields '}
        return render(request,'contest/create.html', context)


@login_required(login_url='/contest/auth/')
def saveEditContest(request):
    try:
        id = request.POST['id']
        admin = Administrator.objects.get(user=request.user)
        contest = Contest.objects.get(owner_id = admin.id, id = id)
        if contest and contest.enable:
            try:
                name = request.POST['name']
                url = request.POST['url']
                start = request.POST['start']
                end = request.POST['end']
                prize = request.POST['prize']
                if name and url and start and end and prize:
                    matInit = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', start)
                    matEnd = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', end)
                    if matInit is None or matEnd is None:
                        context = {'username': request.user.username,'contest':contest,'username': request.user.username,'message':'Dates must have the format yyy/mm/dd'}
                        return render(request,'contest/create.html', context)

                    valUrl = re.match('[a-zA-Z_0-9]*',url)
                    if valUrl is None:
                        context = {'username': request.user.username,'contest':contest,'message':'Url contest must have only numbers, uppercase letters, lowercase letters, or _'}
                        return render(request,'contest/create.html', context)

                    init = datetime.datetime.strptime(start, "%Y/%m/%d")
                    finish = datetime.datetime.strptime(end, "%Y/%m/%d")
                    contest.prize=prize
                    contest.start_date=init
                    contest.end_date=finish
                    try:
                        image = request.FILES['image']
                        contest.image=image
                    except:
                        pass
                    contest.url=url
                    contest.name=name
                    contest.save()
                    return redirect('/contest/dashboard')
                else:
                    context={'username': request.user.username,'contest':contest,'message':'All fields are mandatory'}
                    return render(request,'contest/create.html', context)
            except:
                context = {'username': request.user.username,'contest':contest,'message':'Exception in validation of fields '}
                return render(request,'contest/create.html', context)
        else:
            context={'username': request.user.username,'message':'The contest is not available'}
            return render(request,'contest/contest.html', context)
    except:
        return redirect('/contest/dashboard')


def contestPublic(request, url):
    try:
        contest = Contest.objects.get(url = url, enable = True)
        if contest and contest.enable:
            allVideos = Video.objects.all().filter(contest = contest, status=2).order_by('-created_date')
            paginator = Paginator(allVideos, 50) # Show 50 contacts per page
            page = request.GET.get('page')
            try:
                videos = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                videos = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                videos = paginator.page(paginator.num_pages)

            context = {'contest':contest,'videos': videos, 'pages': paginator.page_range}
        else:
            context = {'message':'The contest is not available'}
        return render(request, 'contest/contest_public.html', context)
    except:
        context = {'message':'The contest is not available'}
        return render(request, 'contest/contest_public.html', context)


def upload(request, url):
    try:
        contest = Contest.objects.get(url = url, enable = True)
        if contest is not None:
            context = {'contest':contest}
            return render(request, 'contest/upload.html', context)
        else:
            context = {'message':'The contest is not available'}
            return render(request, 'contest/contest_public.html', context)
    except:
        context = {'message':'The contest is not available'}
        return render(request, 'contest/contest_public.html', context)


def saveUpload(request):
    try:
        id = request.POST['id']
        contest = Contest.objects.get(id = id, enable = True)
        if contest is not None:
            #create competitor
            competitor = Competitor(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
            competitor.save()
            #request.FILES['video'].name=contest.id+"_"+datetime.datetime.now()._hour+"_"
            video = Video(message=request.POST['message'], path_original=request.FILES['video'], owner=competitor,
                          status=1, created_date=datetime.datetime.now(), contest=contest)
            video.save()
            convertVideos.delay(request.FILES['video'].name, video.id)
            context = {'contest': contest,'message':'We have received your video, we are processing it in this moment. We will send you an email when the video had been published in the contest.'}
            return render(request, 'contest/upload.html', context)
        else:
            context = {'message':'The contest is not available'}
            return render(request, 'contest/contest_public.html', context)
    except:
        context = {'message':'The contest is not available'}
        return render(request, 'contest/contest_public.html', context)


