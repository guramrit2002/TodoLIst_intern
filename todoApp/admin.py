from django.contrib import admin
from .models import Task,User
# Register your models here.

# setting title of admin and index title 
admin.site.site_title = "To do Admin Area"
admin.site.index_title = "Welcome to the To do Admin Area"

# registering models in admin
admin.site.register(Task)
admin.site.register(User)