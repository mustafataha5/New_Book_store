from django.db import models
import datetime
import bcrypt
import re 

# Create your models here.
class UserManager(models.Manager):
    def user_validation(self,postData): 
        errors = {}
        
        if len(postData['first_name']) < 2: 
            errors['first_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2: 
            errors['last_name'] = 'Last name must be at least 2 characters' 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['email'])) > 0:
             errors['email'] = "Email already used!!"
                    
        
        if len(postData['password']) <8: 
             errors['password'] = 'Password must be at least  8 characters .'
        if postData['password'] != postData['check_password'] : 
            errors['check_password'] = 'Does not match password .'   
        if datetime.datetime.strptime(postData['birthday'],'%Y-%m-%d').date() > datetime.date.today() :
            errors['birthday'] ='Birthday must be in past.'
            
        days =  datetime.datetime.strptime(postData['birthday'],'%Y-%m-%d').date()-datetime.date.today()   
        if  days.days > 0 and days.days < 13*365:
            errors['birthday'] ='You must be at least 13 old year.'
        return errors
    
    
    def login_validation(self,postData): 
        errors= {}
        
        if len(User.objects.filter(email=postData['email'])) == 0 : 
            errors['login_email'] = "Wrong email address "
            errors['login_password'] = "Wrong password"
        else: 
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()) : 
                errors['login_password'] = "Wrong password"
        return errors
    
    def update_validation(self,postData,userID): 
        errors = {}
        if len(postData['first_name']) < 2: 
            errors['first_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2: 
            errors['last_name'] = 'Last name must be at least 2 characters' 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        user = User.objects.get(id=userID)    
        check_user = User.objects.filter(email=postData['email'])   
        if len(check_user) == 1 and not user in  check_user.all():
             errors['email'] = "Email already used!by other user!"
        if len(postData['address']) < 2 : 
            errors['address'] = 'Address must be at least 2 characters'
        if len(postData['phone']) < 10 : 
            errors['phone'] = 'Phone must be at least 10 characters'    
        return errors    

class PostManager(models.Manager):
    def post_validation(self,postData):
        errors ={}
       # print("*"*80,postData)
        if len(postData['post_message']) ==0 :
            errors['error_post_message'] = 'Please fill the Post message field'
        return errors 
    def can_delete(self,postID): 
        # post = Post.objects.get(id=postID)
        # pass_time =  abs(post.updated_at.timestamp() - datetime.datetime.timestamp(datetime.datetime.today())) 
        # print("Pass ->>>>>>>>>>>>>>>>. ********",pass_time )
        # print(pass_time < 30*60)
        #return pass_time < 30*60 # 30 min 
        return True
        


class BookManager(models.Manager):
    def book_validation(self,postData): 
        errors = {}
        
        
        
        return errors

class OrderManger(models.Manager):
    def order_validation(self,postData): 
        errors = {}

        
        
        return errors   
    def has_open_order(self,userID):
        orders = Order.objects.filter(user__id=userID)
        if len(orders) > 0 : 
            for i in orders: 
                if i.confirm_buy == False : 
                    return True
        return False 

class CommentManger(models.Manager):
    def comment_validation(self,postData,postID,userID): 
        errors ={}
        if len(postData['comment_message']) == 0 :
            errors['comment_message-'+str(userID)+str(postID)] = 'Please fill the comment message field'
        
        return errors   
    

class CategoryManger(models.Manager):
    def category_validation(self,postData): 
        errors = {}
        
        
        
        return errors  
    

class LanguageManger(models.Manager):
    def language_validation(self,postData): 
        errors = {}
        # if len(postData['review_message']) == 0 :
        #     errors['review_message'] = 'Please fill the review message field'
          
        
        return errors    
        
          
    
class ReviewManger(models.Manager):
    def review_validation(self,postData,userId,bookID): 
        errors = {}
       
        if int(postData['review_level']) == 0 : 
            errors['review_level'] = "Please choose your review level"  
        if len(Review.objects.filter(user__id=userId))>0 and len(Review.objects.filter(book__id=bookID)):
             errors['review_level'] = "You can not review book more than one , You can edit pervious "  
        return errors  
    def review_ajax_validation(self,postData): 
        errors = {}
       
        if int(postData['review_level']) == 0 : 
            errors['review_level'] = "Please choose your review level"  
        if len(Review.objects.filter(user__id=postData['userID'],book__id=postData['bookID']))>0 :
             errors['review_level'] = "You can not review book more than one "  
        return errors     


class User(models.Model): 
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=7)
    phone = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=255,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
 

class Post(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    objects = PostManager()


class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    objects = CommentManger()



class Category(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManger()


class Language(models.Model):
    name = models.CharField(max_length=45)
    objects = LanguageManger()
    
class Author(models.Model): 
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
class Book(models.Model): 
    title = models.CharField(max_length=45)
    description = models.TextField()
    number_of_pages = models.IntegerField()
    url_image = models.TextField()
    price = models.FloatField()
    author = models.ForeignKey(Author,related_name='books',on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='books', on_delete=models.CASCADE)
    liked_by_users= models.ManyToManyField(User,related_name='likes_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()



class Order(models.Model):
    confirm_buy = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    books= models.ManyToManyField(Book,related_name='orders')
    objects = OrderManger()
    
class Review (models.Model): 
    user = models.ForeignKey(User,related_name='reviews', on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='reviews', on_delete=models.CASCADE) 
    review_level = models.IntegerField()
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = ReviewManger() 











