from django.shortcuts import render , redirect
from .models import User,Book,Post,Comment, Category,Order,Review,Author

from django.db.models import Q 

from django.db import models
from  django.contrib import messages
from django.http import JsonResponse
import bcrypt
import json
import datetime
import math

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
    
    
def get_total_order(order): 
    total = 0
    if(order == ''): 
        return 0
    for book in order.books.all(): 
        total = total + book.price 
    return math.floor(total * 100)/100.0     
def show_book(request,bookID):
    
    book = Book.objects.get(id=bookID)
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID']))  
    
    if not 'userID' in request.session :  
        data = {
            'book': book,
            'reviews': book.reviews.all(),
            'order':order , 
            'total':get_total_order(order)
            }
    else: 
        
               
        data = {'book': book,
            'reviews': book.reviews.all(),
            "user":User.objects.get(id=request.session['userID']),
             'order':order , 
             'total':get_total_order(order)
            }
    return render (request, 'book_details.html', data)


def contact(request): 
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 
    data ={
        'total': get_total_order(order),
    }    
    
    return render(request,'contact_about.html',data)


def main(request):

   
        #return render(request,'user_main_page.html',data)
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID']))  
    
    review =Review.objects.all()
    #populer = review.values('book_id').annotate(review_count=models.Count('book_id'),sum_level=models.Sum('review_level')).order_by('-review_count')[:10]
    populer = review.values('book_id').annotate(review_count=models.Count('book_id')).order_by('-review_count')[:8]
    pupuler_book = Book.objects.filter(id__in=populer.values('book_id')) 
   # print('-------------',review)
   # print('-------------',pupuler_book)
    favorite_book = Book.liked_by_users.through.objects.all()
    favorite_book_ids = favorite_book.values('book_id').annotate(review_count=models.Count('book_id')).order_by('-review_count')[:8]
    favorite_books = Book.objects.filter(id__in=favorite_book_ids.values('book_id'))
    data= {}
    if  not ('userID' in request.session) : 
       
        data = { 'favorite_books': favorite_books , 
                'order' : order ,
                'total': get_total_order(order),
                'pupuler_book': pupuler_book,
                }
    else :
        
        data = {
            "user":User.objects.get(id=int(request.session['userID'])),
            #'books' : Book.objects.all(), 
            'favorite_books': favorite_books , 
            'order' : order ,
            'total': get_total_order(order),
            'pupuler_book': pupuler_book,
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
       
        reviews = book.reviews.all().order_by('-updated_at').values() 
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
        messages.error(request,'You need to regiester or login',extra_tags='invalid_accuess')
        return redirect('/login')
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 
    data={
        "user":User.objects.get(id=request.session['userID']),
        "posts":Post.objects.all().order_by('-updated_at'),
        "total":get_total_order(order),
    } 
    return render(request,'new_wall.html',data)



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



def add_to_cart(request,bookID,fromID):
    
    
    print(">>>>>>>",(not 'userID' in request.session) )
    if not 'userID' in request.session: 
        print(">>>>>>> Need to login" )
        messages.error(request,'Need to Login/SignUp')
        if (fromID == 5): 
            return JsonResponse({'error':10})
        return redirect('/login') 
    
    userID = int(request.session['userID'])
    user = User.objects.get(id=userID)
    book = Book.objects.get(id=bookID)
    if ( not 'orderID' in request.session):
        order = Order.objects.create(user=user)
        order.books.add(book)
        #request.session['total'] = book.price
        request.session['orderID']= order.id 
    else: 
        order = Order.objects.get(id=int(request.session['orderID']))
        order.books.add(book) 
    if fromID == 2 :      
        return redirect(f'/book/{bookID}')
    elif fromID == 3 : 
        return redirect('/category')
    elif fromID == 5 : 
        data = {'total_item':len(order.books.all()),
                'total':get_total_order(order),}
        return JsonResponse(data)
    else: 
        return redirect('/')

# def add_to_cart_main(request,bookID):
#     if not 'userID' in request.session: 
#         messages.error(request,'Need to Login/SignUp')
#         return redirect(f'/login') 
    
#     userID = int(request.session['userID'])
#     user = User.objects.get(id=userID)
#     book = Book.objects.get(id=bookID)
#     if ( not 'orderID' in request.session):
#         order = Order.objects.create(user=user)
#         order.books.add(book)
#         request.session['orderID']= order.id 
#     else: 
#         order = Order.objects.get(id=int(request.session['orderID']))
#         order.books.add(book)  
#     return redirect('/')
           

def delete_book_from_order(request,bookID,fromID):
    if not 'userID' in request.session or  not 'orderID' in request.session: 
        messages.error(request,'No order yet , Need to Login/SignUp')
        return redirect(f'/login') 
    userID = int(request.session['userID'])
    orderID = int(request.session['orderID'])
    order = Order.objects.get(id=orderID)
    book = Book.objects.get(id=bookID)
    order.books.remove(book)
    
    if len(order.books.all()) == 0 : 
        order = Order.objects.get(int(request.session['orderID']))
        order.delete() 
        del request.session['orderID'] 
    if fromID == 2 :
        return redirect(f'/book/{bookID}')
    elif fromID == 4: 
         return redirect(f'/user/{userID}')
    elif fromID == 3 : 
        return redirect('/category')  
    elif fromID == 5 : 
        data = {'total_item':len(order.books.all()),
                'total':get_total_order(order),}
        return JsonResponse(data)   
    else: 
        return redirect('/')


def confirm_order(request): 
    if not 'userID' in request.session :
        messages.error(request,'No order yet , Need to Login/SignUp')
        return redirect(f'/login')  
    
    userID = request.session['userID']
    if  not 'orderID' in request.session: 
        messages.error(request,'No order yet')
        return redirect(f'/user/{userID}')
    if  'orderID' in  request.session :  
        order = Order.objects.get(id=int(request.session['orderID'])) 
        order.confirm_buy = True
        messages.success(request,'Order confirmed, please check your email')
        del request.session['orderID']
        return redirect(f'/user/{userID}')
















# display books in categories(categories page)

def cat(request):
    categories = Category.objects.all()
    
    if not 'userID' in request.session:
        data = {
            'categories': categories,
        }
        return render(request, 'catergories.html', data)
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 

        
    
    data = {
        "user": User.objects.get(id=request.session['userID']),
        'categories': categories,
        'order':order , 
        'total' : get_total_order(order),
    }
    
    return render(request, 'catergories.html', data)


# view user profile
def account(request, userID):
    if not 'userID' in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userID'])
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 
    
    context = {
        'user': user ,
        'order': order , 
        'total' : get_total_order(order),
    }

    return render(request, 'profile.html', context)

def edit_user(request):
    if not 'userID' in request.session:
        messages.error(request,'Please Loing/SignUp !')
        return redirect('/login')
    user = User.objects.get(id=request.session['userID'])
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 
    
    data = {
        'user': user ,
        'order': order , 
        'total' : get_total_order(order),
    }
    return render (request, 'editprofile.html',data)

def update_user(request):
    if not 'userID' in request.session:
        messages.error(request,'Please Loing/SignUp !')
        return redirect('/login')
    userID = request.session['userID']
    errors = User.objects.update_validation(request.POST,userID)
    if len(errors): 
        for key,val in errors.items():
            messages.error(request,val,extra_tags=key)
        return redirect('/user/edit')
     
    
    user = User.objects.get(id=userID) 
    
    user.email = request.POST['email']
    user.first_name = request.POST['first_name'].capitalize()
    user.last_name = request.POST['last_name'].capitalize()
    user.address = request.POST['address'].capitalize()
    user.phone = request.POST['phone']
    user.save()
    return redirect(f'/user/{userID}')
    

def checkout(request):
    pass



def search(request): 
    return render(request,'search.html')
    
def get_info_search(request):
    
    if request.method == "POST": 
        # errors= Book.objects.validate() 
        books = ''
        query = request.POST['data']
        typeID = int(request.POST['typeID'])
        if len(query) > 50 : 
            messages.error('Search can not be more than 50 characters')
        
        if typeID == 1: 
            #books = Book.objects.filter(title__istartswith=query)
            books = Book.objects.filter(title__icontains=query)
            authors = {}
            for i in books: 
                authors[i.id] = i.author.first_name+" "+i.author.last_name 
            data = {
            'books_list': list(books.values()) , 
            'authors_list': authors,
            }    
        elif typeID == 2 : 
             authors = Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) )
             #books = Book.objects.filter(author_id__in=authors.values('id'))         
             data = {
              #  'books_list': list(books.values()) , 
                'authors_list': list(authors.values()),
            }
        return JsonResponse(data)







































































































def about(request):

    if  not 'userID' in request.session : 
        
        return render (request, 'contact_about.html')
        #return render(request,'user_main_page.html',data)
    if not 'orderID' in  request.session : 
        order = '' 
    else: 
        order = Order.objects.get(id=int(request.session['orderID'])) 

    data = {
        "user":User.objects.get(id=request.session['userID']),
        'total': get_total_order(order)
    }
    return render (request, 'contact_about.html',data)
#add to favitore books
def add_fev_book(request, bookID):
    if not 'userID' in request.session: 
        messages.error(request,'Need to Login/SignUp')
        return redirect(f'/login')
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




