from django.shortcuts import render , redirect
from .models import User
from  django.contrib import messages
import bcrypt
import datetime
# Create your views here.

def index (request): 
    if  not 'userID' in request.session : 
        return render(request,'user_main_page.html')
    data = {'user': User.objects.get(id=int(request.session['userID']))}
    return render(request,'user_main_page.html',data) 




def register(request): 
    return render(request,'registeration.html')
    
    
def login(request):
    return render(request,'login.html')
 
def check_login(request):
      if request.method == 'POST': 
        errors = User.objects.login_validation(request.POST)
        if len(errors) > 0 : 
            for key,val in  errors.items(): 
                messages.error(request,val,extra_tags=key)
                return redirect('app:login')
        user = User.objects.get(email=request.POST['email'])    
        request.session['userID'] = user.id    
        return redirect('app:index')    
 
def create_user(request): 
    
    if request.method == 'POST': 
        errors = User.objects.user_validation(request.POST)
        if len(errors) > 0 : 
            for key,val in  errors.items(): 
                messages.error(request,val,extra_tags=key)
            return redirect('app:register')
        
        user_fname = request.POST['first_name']
        user_lname = request.POST['last_name']
        user_email = request.POST['email']
        password =bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        brithday =request.POST['birthday']
        gender = request.POST['gender']
        user = User.objects.create(first_name=user_fname,last_name=user_lname,email=user_email,gender=gender,birthday=brithday,password=password)
        request.session['userID'] = user.id
        return redirect('app:index')  
    
    
def logout(request):
    if 'userID' in request.session :  
        request.session.clear()
    return redirect('app:index')         
    
    





