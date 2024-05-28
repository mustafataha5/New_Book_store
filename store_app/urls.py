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
    path('contact',views.about),
    path('main', views.main,name='main'),
    path('wall',views.main_wall,name='wall'),
    path('addPost',views.add_post),
    path('addComment/<int:postID>',views.add_comment),
    path('deletePost/<int:postID>',views.delete_post),
    path('create_review/<int:bookID>',views.create_review),
    path('ajax/<int:bookID>',views.get_ajax),
    








path('category', views.cat),
]