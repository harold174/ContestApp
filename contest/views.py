from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Administrator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from .forms import ProfileImageForm
from .models import ProfileImage


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
            print("User is valid, active and authenticated")
            return render(request, 'contest/dashboard.html')
        else:
            error="The password is valid, but the account has been disabled!"
    else:
        # the authentication system was unable to verify the username and password
        error="The username and password were incorrect."

    context = {'error_auth': error}
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

def dashboard(request):
    return render(request, 'contest/dashboard.html')

def createContest(request):
    return render(request, 'contest/create.html')

def showContest(request):
    return render(request, 'contest/contest.html')

def contestPublic(request, id):
    return render(request, 'contest/contest_public.html')

def upload(request, id):
    return render(request, 'contest/upload.html')


class ProfileImageView(FormView):
    template_name = 'contest/profile_image_form.html'
    form_class = ProfileImageForm

    def form_valid(self, form):
        profile_image = ProfileImage(
            image=self.get_form_kwargs().get('files')['image'])
        profile_image.save()
        self.id = profile_image.id

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile_image', kwargs={'pk': self.id})


class ProfileDetailView(DetailView):
    model = ProfileImage
    template_name = 'contest/profile_image.html'
    context_object_name = 'image'


class ProfileImageIndexView(ListView):
    model = ProfileImage
    template_name = 'contest/profile_image_view.html'
    context_object_name = 'images'
    queryset = ProfileImage.objects.all()