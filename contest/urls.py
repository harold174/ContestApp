from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'auth/', views.auth, name='auth'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logoutView, name='logout'),
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'dashboard/new/$', views.createContest, name='create'),
    url(r'dashboard/save/$', views.saveCreateContest, name='save'),
    url(r'dashboard/edit/(?P<id>[0-9]+)$', views.editContest, name='edit'),
    url(r'dashboard/edit/save/$', views.saveEditContest, name='saveEdit'),
    url(r'dashboard/show/(?P<url>[a-zA-Z0-9_]+)$', views.showContest, name='show'),
    url(r'dashboard/delete/(?P<id>[0-9]+)$', views.deleteContest, name='delete'),
    url(r'play/(?P<id>[a-zA-Z0-9_]+)/$', views.contestPublic, name='contestPublic'),
    url(r'play/(?P<id>[a-zA-Z0-9_]+)/upload/$', views.upload, name='upload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
