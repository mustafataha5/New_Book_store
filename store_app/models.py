from django.db import models
import datetime
import bcrypt
import re 

# Create your models here.
class UserManager(models.Manager):
    def user_validation(self,postData): 
        errors = {}
        
        if len(postData['first_name']) < 2: 
            errors['first_name'] = 'First name must be at least 2 charcter'
        if len(postData['last_name']) < 2: 
            errors['last_name'] = 'Last name must be at least 2 charcter' 
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

class PostManager(models.Manager):
    def post_validation(self,postData): 
        errors = {}
        
        
        
        return errors 
        


class BookManager(models.Manager):
    def book_validation(self,postData): 
        errors = {}
        
        
        
        return errors

class OrderManger(models.Manager):
    def order_validation(self,postData): 
        errors = {}
        
        
        
        return errors   


class CommentManger(models.Manager):
    def comment_validation(self,postData): 
        errors = {}
        
        
        
        return errors  
    

class CategoryManger(models.Manager):
    def category_validation(self,postData): 
        errors = {}
        
        
        
        return errors  
    

class LanguageManger(models.Manager):
    def language_validation(self,postData): 
        errors = {}
        
        
        
        return errors  


class User(models.Model): 
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=7)
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
    liked_by_users= models.ManyToManyField(User,related_name='likes_books',)
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
    users = models.ForeignKey(User,related_name='reviews', on_delete=models.CASCADE)
    books = models.ForeignKey(Book,related_name='reviews', on_delete=models.CASCADE) 
    review_level = models.IntegerField()
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   











