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
    my_product = models.get_sta() 
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name = request.POST.get('product_name', 'Unknown Product')
      
        total = price * num_product

       
        purchases = request.session.get('purchases', [])
        
       
        purchase = {
            'product_name': product_name,
            'num_product': num_product,
            'price': price,
            'total': total,
           
        }
        purchases.append(purchase)
        
       
        request.session['purchases'] = purchases
        
        return redirect('/purchase')
    
    return render(request, 'Stationery.html', {'my_product': my_product})


def toys(request):
    my_product = models.get_toy() 
    if request.method == 'POST':
        price = float(request.POST.get("price", 0))
        num_product = int(request.POST.get('num_product', 0))
        product_name = request.POST.get('product_name', 'Unknown Product')
      
        total = price * num_product

       
        purchases = request.session.get('purchases', [])
        
       
        purchase = {
            'product_name': product_name,
            'num_product': num_product,
            'price': price,
            'total': total,
           
        }
        purchases.append(purchase)
        
       
        request.session['purchases'] = purchases
        
        return redirect('/purchase')
    return render(request, 'Stationery.html', {'my_product': my_product})


def purchase(request):
    purchases = request.session.get('purchases', [])
    
    # Use the last purchase for display (for the "Are you sure" page)
    last_purchase = purchases[-1] if purchases else None

    context = {
        'purchase': last_purchase
    }
    
    return render(request, 'purchase.html', context)

'purchase.html'

def order(request):
  purchases = request.session.get('purchases', [])
  return render(request, 'main.html', {'purchases': purchases})
    


def logout(request):
    request.session.flush()
    return redirect('/') 