from django.shortcuts import render ,redirect
from . import models
from .models import user 
from django.contrib import messages 
import bcrypt


def index(request):
    return render(request , 'main.html' )

def about_us(request):
    return render(request , 'about_us.html')

def register(request):
    if request.method == 'POST':
        errors = models.user.objects.val(request.POST)
        if len(errors) > 0: 
                for key , value in errors.items():
                  messages.error(request , value)
                return redirect('/')
        else:    
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(pw_hash) 
            users = models.create_user(request.POST , pw_hash = pw_hash ) 
            messages.success(request , 'the show user successfuly created !!')
            request.session['user_id'] = users.id
            request.session['First_name'] = users.First_name
            request.session['Last_name'] = users.Last_name 
            return redirect('/')
    return render(request , 'login_register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']        
        users =  user.objects.filter(email = email).first()
        if users and bcrypt.checkpw(request.POST['password'].encode(), users.password.encode()):
            request.session['user_id'] = users.id  
            request.session['First_name'] = users.First_name
            request.session['Last_name'] = users.Last_name   
            return redirect('/main')
        else:   
            return render(request,'main.html')


def Stationery(request):
    return render(request , 'Stationery.html' ) 

def toys(request):
    return render(request , 'toys.html' ) 

def purchase(request):
    return render(request , 'purchase.html' ) 

def logout(request):
    request.session.clear()
    return redirect('/')