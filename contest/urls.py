from django.conf.urls import url
from .views import ProfileImageView, ProfileDetailView
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'auth/', views.auth, name='auth'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logoutView, name='logout'),
    url(r'dashboard/new/$', views.createContest, name='create'),
    url(r'dashboard/show/$', views.showContest, name='show'),
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'play/(?P<id>[a-zA-Z0-9_]+)/$', views.contestPublic, name='contestPublic'),
    url(r'play/(?P<id>[a-zA-Z0-9_]+)/upload/$', views.upload, name='upload'),
    url(r'^upload/', ProfileImageView.as_view(), name='profile_image_upload'),
    url(r'^uploaded/(?P<pk>\d+)/$', ProfileDetailView.as_view(),name='profile_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
