from django.urls import path,include
from . import views 

app_name = 'app'


urlpatterns = [
    path('',views.index , name = 'index'),
    path('login',views.login,name='login'),
    path('register',views.register, name='register'),
    path('login',views.login), 
    path('logout',views.logout),
    path('check_login',views.check_login),
    path('create_user',views.create_user), 
    path('book/<int:bookID>',views.show_book),
    path('contact',views.contact),
<<<<<<< HEAD
    path('main', views.main),
    
=======
    path('main', views.main,name='main'),
>>>>>>> master

]