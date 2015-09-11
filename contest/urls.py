from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'auth/', views.auth, name='auth'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),

]