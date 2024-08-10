from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages 
from django.http import JsonResponse
from .models import user , product
import bcrypt


def index(request):
    First_name = request.session.get('First_name')
    Last_name = request.session.get('Last_name')
    purchases = request.session.get('purchases', [])
    context = { 
        'First_name' : First_name,
        'Last_name' : Last_name ,
        'purchases': purchases
    }
    return render(request, 'main.html', context )

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
            users = models.create_user(request.POST , pw_hash = pw_hash) 
            messages.success(request , 'the user successfuly created !!')
            request.session['First_name'] = users.First_name
            request.session['Last_name'] = users.Last_name 
            return redirect('/')
    return render(request , 'login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
       
        users = models.user.objects.filter(email=email).first()
        
    
        if users and bcrypt.checkpw(password.encode(), users.password.encode()):
            request.session['First_name'] = users.First_name
            request.session['Last_name'] = users.Last_name   
            First_name = request.session.get('First_name')
            Last_name = request.session.get('Last_name')
            return render(request, 'main.html' , {'First_name' : First_name , 'Last_name' : Last_name})
        else:   
            messages.error(request, 'Invalid email or password')
            return redirect('/')
    return render(request, 'login.html')



def Stationery(request): 
    my_product = models.get_sta()
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name = request.POST.get('product_name', 'Unknown Product')
        total = price * num_product
  
        current_purchase = {
            'product_name': product_name,
            'num_product': num_product,
            'price': price,
            'total': total,
        } 
        request.session['current_purchase'] = current_purchase
        return redirect('/purchase') 
    return render(request, 'Stationery.html', {'my_product': my_product})


def toys(request):
    my_product = models.get_toy() 
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name = request.POST.get('product_name', 'Unknown Product')
       
        total = price * num_product
        current_purchase = {
            'product_name': product_name,
            'num_product': num_product,
            'price': price,
            'total': total,
          
        } 
        request.session['current_purchase'] = current_purchase
        return redirect('/purchase')
    return render(request, 'Stationery.html', {'my_product': my_product})


def purchase(request):
    current_purchase = request.session.get('current_purchase', None)
    context = {
        'purchase': current_purchase
    }
    return render(request, 'purchase.html', context)



def order(request):
    current_purchase = request.session.get('current_purchase', None)
    if current_purchase:
        purchases = request.session.get('purchases', [])
        purchases.append(current_purchase)      
        request.session['purchases'] = purchases      
        del request.session['current_purchase']    
    return redirect('/main')
    

def delete_purchase(request, index):
    if request.method == 'POST':
        purchases = request.session.get('purchases', [])
        if 0 <= index < len(purchases):
            purchases.pop(index)
            request.session['purchases'] = purchases
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def logout(request):
    request.session.flush()
    return redirect('/') 