from django.urls import path     
from . import views
from django.contrib import admin
urlpatterns = [
    path('', views.register , name='register'),
    path('login', views.login , name='login'),
    path('main', views.index), 
    path('Stationery', views.Stationery , name='Stationery'),
    path('toys', views.toys , name='toys'),
    path('purchase', views.purchase , name='purchase'),
    path('about_us', views.about_us , name='about_us'),
    path('logout', views.logout , name='logout'),
    path('admin/', admin.site.urls),
          ]

