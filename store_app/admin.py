from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Book)

