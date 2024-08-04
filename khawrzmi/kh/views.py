from django.shortcuts import render ,redirect
from . import models
from .models import user ,product
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
    my_product = product.objects.all()
    if request.method == 'POST': 
        price = request.POST['price']
        num_product = request.POST['num_product']
        total = price * num_product
        product.objects.create(num_product = num_product , total = total) 
        request.session['total'] = total
        request.session['num_product'] = num_product
        request.session['price'] = price 
        return redirect('/purchase')
    return render(request , 'Stationery.html' , {'my_product' : my_product}) 

def toys(request):
    return render(request , 'toys.html' ) 

def purchase(request):
    if request.method == 'POST': 
        price =  request.session.get('price')
        num_product = request.session.get('num_product')
        total = request.session.get('total')
        # context = {
        #     'price' : price,
        #     'num_product' : num_product,
        #     'total' : total
        # }
    return render(request , 'purchase.html',{'price' : price , 'num_product' :num_product , 'total' :total} ) 


def products(request):
    my_product = product.objects.all() 
    return render(request , 'Stationery.html' , {'my_product' : my_product})



def logout(request):
    request.session.clear()
    return redirect('/')