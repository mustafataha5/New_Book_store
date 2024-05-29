from django.urls import path,include
from . import views 

app_name = 'app'


urlpatterns = [
    path('',views.index , name = 'index'),
    path('login',views.login,name='login'),
    path('register',views.register, name='register'),
    path('login',views.login), 
    path('logout/',views.logout),
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
    path('ajax/review/create',views.ajax_create_review),
    path('ajax/review/delete',views.ajax_delete_review),
    path('add_to_cart',views.add_to_cart),
  




    path('category', views.cat),

    path('user/<int:userID>',views.account) ,  




















path('categories', views.cat,),
path('user/<int:user>', views.account),
path('addFav/<int:bookID>', views.add_fev_book),
path('removeFav/<int:bookID>', views.unfav_book),
path('user/<int:userID>/edit', views.edit),
path('checkout', views.checkout),


]