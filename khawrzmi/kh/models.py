from django.db import models
import re	
import bcrypt

class UserManager(models.Manager):
    def val(self , postData ):
        errors = {}
        if len(postData['First_name']) < 2:
            errors['First_name'] = 'First_name should be at least 2 charcters'

        if len(postData['Last_name']) < 2:
            errors['password'] = 'Last_name should be at least 2 charcters'  

        if len(postData['password']) < 8:
            errors['password'] = 'password should be at least 8 charcters'   

        if len(postData['conf_password']) < 8:
            errors['conf_password'] = 'conf_password should be at least 8 charcters'      

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        if len(postData['password']) !=  len(postData['conf_password']):
            errors['conf_password'] = "passwords do not match"
            
        if user.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists."

        return errors 


class user(models.Model):
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    email = models.CharField(max_length= 30)
    password = models.CharField(max_length=30)
    conf_password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class product(models.Model):
    name_product = models.CharField(max_length=30)
    price = models.FloatField()
    image = models.ImageField(upload_to='img')
    created_at = models.DateTimeField(auto_now_add=True)
    num_product = models.IntegerField() 
    total = models.FloatField()
    pro = models.ManyToManyField(user,related_name='my_product' )


def create_user(request , pw_hash):
    First_name = request['First_name']
    Last_name = request['Last_name']
    email = request['email']
    password = request['password']
    conf_password = request['conf_password']
    return user.objects.create(First_name = First_name , Last_name = Last_name , email = email ,  conf_password = pw_hash , password = pw_hash)

def get_all():
    return product.objects.filter(id__gte=1, id__lte=9)

def deletee(id):
    a = product.objects.get(id = id)
    a.delete()