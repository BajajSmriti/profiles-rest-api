from django.contrib import admin
from profiles_api import models

# Register your models here. so that we can manage objects in the (db model)table thru django admin interface
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
