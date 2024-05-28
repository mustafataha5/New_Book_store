from django.shortcuts import render , redirect,HttpResponse
from .models import User,Book,Post,Comment, Category

from .models import User,Book,Post,Comment,Review


from  django.contrib import messages
from django.http import JsonResponse
import bcrypt
import json
import datetime
# Create your views here.

def index (request): 
    # test
    # if  not 'userID' in request.session : 
    #     data = { 'books': Book.objects.all(),}
    #     return redirect('app:main')
    #     #return render(request,'user_main_page.html',data)
    # data = {
    #     'user': User.objects.get(id=int(request.session['userID'])),
    #     'books': Book.objects.all(),
    # }
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
        
        user_fname = request.POST['first_name'].capitalize()
        user_lname = request.POST['last_name'].capitalize()
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
    
    book = Book.objects.get(id=bookID)
    
    if not 'userID' in request.session :  
        data = {'book': book,
            'reviews': book.reviews.all(),
            
            }
    else: 
        data = {'book': book,
            'reviews': book.reviews.all(),
            "user":User.objects.get(id=request.session['userID']),
            }
    return render (request, 'book_details.html', data)


def contact(request): 
    return render(request,'contact_about.html')


def main(request):

    if  not 'userID' in request.session : 
        data = { 'books': Book.objects.all(),}
        return render (request, 'the_main_page.html',data)
        #return render(request,'user_main_page.html',data)


    data = {
        "user":User.objects.get(id=request.session['userID']),
        'books' : Book.objects.all(), 
    }
    return render (request, 'the_main_page.html',data)



def get_ajax(request,bookID):
    book = Book.objects.get(id=bookID) 
    reviews = book.reviews.all().values() 
    user_ids = book.reviews.all().values('user') 
    users = User.objects.filter(id__in=user_ids).values('id','first_name','last_name')
    data = {
                'reviews_list' : list(reviews ),
                'user_list' : list(users)  ,
            }
    #data_json = json.dumps(reviews_list)
    return JsonResponse(data,safe=False)


def ajax_create_review(request): 
    if request.method == 'POST' and request.is_ajax():
        # Process the posted data
        #print("====================",request.POST)
        errors = Review.objects.review_ajax_validation(request.POST)
        
        bookID = request.POST['bookID']
        if len(errors):
            data = {
                'error': errors['review_level'] , 
            }
            return JsonResponse(data,safe=False) 

        userID = request.POST['userID']
        review_message = request.POST['message']
        review_level = request.POST['review_level']
        book = Book.objects.get(id=bookID) 
        user = User.objects.get(id=userID)
        #Review.objects.create(message=review_message,review_level=review_level,user=user,book=book)
        Review.objects.create(message=review_message,review_level=review_level,user=user,book=book)
       
        reviews = book.reviews.all().values() 
        user_ids = book.reviews.all().values('user') 
        users = User.objects.filter(id__in=user_ids).values('id','first_name','last_name')
        data = {
                'reviews_list' : list(reviews ),
                'user_list' : list(users)  ,
            }
        return JsonResponse(data,safe=False)

def create_review(request,bookID): 
    
    if request.method == 'POST': 
        if not 'userID' in request.session: 
            return redirect(f'/book/{bookID}')
        userID= int(request.session['userID'])
        
        errors = Review.objects.review_validation(request.POST,userID,bookID)
        
             
        if len(errors) > 0 : 
            for key,val in errors.items() : 
                messages.error(request,val,extra_tags=key)
            return redirect(f'/book/{bookID}')
           # return redirect('ajax')
           
        rev_message = request.POST['review_message']
        rev_level = request.POST['review_level']
        user = User.objects.get(id=userID)
        book = Book.objects.get(id=bookID)
        Review.objects.create(message=rev_message,review_level=rev_level,user=user,book=book)
    return redirect(f'/book/{bookID}')

    #return redirect(f'/ajax/{bookID}')   

def ajax_delete_review(request):
    if request.method == 'POST' and request.is_ajax():
        if not 'userID' in request.session: 
            return redirect('/login')
        
 
        reviewID = request.POST['reviewID']
        
        review = Review.objects.get(id=reviewID)
        book = Book.objects.get(id=review.book.id)
        review.delete()
        reviews = book.reviews.all().values() 
        user_ids = book.reviews.all().values('user') 
        users = User.objects.filter(id__in=user_ids).values('id','first_name','last_name')
        data = {
                'reviews_list' : list(reviews ),
                'user_list' : list(users)  ,
            }
        return JsonResponse(data,safe=False)
    data = {
                'message': f'Error :can not  delete review ' , 
            }
    return JsonResponse(data,safe=False)
    





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































# display books in categories(categories page)

def cat(request):
    categories = Category.objects.all()
    
    if not 'userID' in request.session:
        data = {
            'categories': categories,
        }
        return render(request, 'the_main_page.html', data)
    
    data = {
        "user": User.objects.get(id=request.session['userID']),
        'categories': categories,
    }
    
    return render(request, 'catergories.html', data)



# view user profile
def account(request, userID):
    if not 'userID' in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userID'])
    context = {
        'user': user ,
    }

    return render(request, 'profile.html', context)




    

    








































































































def about(request):

    if  not 'userID' in request.session : 
        data = { 'books': Book.objects.all(),}
        return render (request, 'contact_about.html',data)
        #return render(request,'user_main_page.html',data)
  

    data = {
        "user":User.objects.get(id=request.session['userID']),
        'books' : Book.objects.all(), 
    }
    return render (request, 'contact_about.html',data)
#add to favitore books
def add_fev_book(request, bookID):
    user = User.objects.get(id=request.session['userID'])
    book = Book.objects.get(id=bookID)
    book.liked_by_users.add(user)

    return redirect (f'/book/{bookID}')
#remove book  from favitore books
def unfav_book(request, bookID):
    user = User.objects.get(id=request.session['userID'])
    book = Book.objects.get(id=bookID)
    book.liked_by_users.remove(user)

    return redirect (f'/book/{bookID}')




