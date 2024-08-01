from django.urls import path     
from . import views
urlpatterns = [
    path('', views.register , name='register'),
    path('login', views.login , name='login'),
    path('main', views.index), 
    path('Stationery', views.Stationery , name='Stationery'),
    path('toys', views.toys , name='toys'),
    path('about_us', views.about_us , name='about_us'),
    path('logout', views.logout , name='logout'),

          ]
