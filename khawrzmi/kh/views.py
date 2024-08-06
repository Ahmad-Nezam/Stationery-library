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
    my_product = product.objects.filter(id__gte=1, id__lte=9)
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name  = request.POST.get('product_name', 'Unknown Product')

        total = price * num_product

      
        request.session['total'] = total
        request.session['num_product'] = num_product
        request.session['price'] = price
        request.session['product_name'] = product_name 

        return redirect('/purchase') 
    return render(request, 'Stationery.html', {'my_product': my_product})


def toys(request):
    my_product = product.objects.filter(id__gte=1, id__lte=6)
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name  = request.POST.get('product_name', 'Unknown Product')

        total = price * num_product

      
        request.session['total'] = total
        request.session['num_product'] = num_product
        request.session['price'] = price
        request.session['product_name'] = product_name 

        return redirect('/purchase') 
    return render(request, 'Stationery.html', {'my_product': my_product})


def purchase(request):
        price = request.session.get('price' , None)
        num_product = request.session.get('num_product', None)
        total = request.session.get('total', None)
        product_name  = request.session.get('product_name', None)
    
        return render(request, 'purchase.html', {'price' : price, 'num_product': num_product, 'total': total, 'product_name' : product_name })


def order(request):
    price = request.session.get('price', None)
    num_product = request.session.get('num_product', None)
    total = request.session.get('total', None)
    name_product  = request.session.get('product_name', None) 
   
    return render(request, 'main.html', {'price': price, 'num_product': num_product, 'total': total, 'product_name' : name_product })


def logout(request):
    request.session.flush()
    return redirect('/') 