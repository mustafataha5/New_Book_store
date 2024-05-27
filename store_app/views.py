from django.shortcuts import render , redirect
from .models import User,Book,Post,Comment
from  django.contrib import messages
import bcrypt
import datetime
# Create your views here.

def index (request): 
    if  not 'userID' in request.session : 
        data = { 'books': Book.objects.all(),}
        return redirect('app:main')
        #return render(request,'user_main_page.html',data)
    data = {
        'user': User.objects.get(id=int(request.session['userID'])),
        'books': Book.objects.all(),
    }
    return redirect('app:main')
    #return render(request,'user_main_page.html',data) 




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
    
    


def show_book(request,bookID):
    data = {'book': Book.objects.get(id=bookID)}

    return render (request, 'book_details.html', data)


def contact(request): 
    return render(request,'contact_about.html')


def main(request):
    
    data = {
         "user":User.objects.get(id=request.session['userID']),
        'books' : Book.objects.all(), 
    }
    
    return render (request, 'the_main_page.html',data)































def main_wall(request):
    if not 'userID' in request.session:
        #messages.warning(request,'You need to regiester or login',extra_tags='invalid_accuess')
        return redirect('/')
    data={
        "user":User.objects.get(id=request.session['userID']),
        "posts":Post.objects.all().order_by('-updated_at'),
    } 
    return render(request,'wall_page.html',data)



def add_post(request):
    if request.method == 'POST': 
        errors = Post.objects.post_validation(request.POST)
        user =User.objects.get(id=request.session['userID']) # for testing
        if len(errors) > 0 : 
            for key,val in errors.items(): 
                messages.error(request,val,extra_tags=key)
        else: 
            Post.objects.create(message=request.POST['post_message'],user=user)       
    return redirect("app:wall")


def add_comment(request,postID):
    if request.method == 'POST': 
        errors = Comment.objects.comment_validation(request.POST,postID,request.session['userID'])
        if len(errors) > 0 : 
            for key,val in errors.items():
                messages.error(request,val,key)
            return redirect("app:wall")   
        post = Post.objects.get(id=postID) 
        user = User.objects.get(id=request.session['userID'])       
        Comment.objects.create(message=request.POST['comment_message'],user=user,post=post)
                
    
    return redirect("app:wall")

def delete_post(request,postID):
    if Post.objects.can_delete(postID) :
        post = Post.objects.get(id=postID)
        post.delete()    
    return redirect("app:wall")


















    