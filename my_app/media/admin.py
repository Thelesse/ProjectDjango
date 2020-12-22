from django.contrib import admin
from .models import *

#this code make admin panel for us to manage our site
admin.site.register(App_User)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Likes)

