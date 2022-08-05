from django.contrib import admin

from .models import UserProfile, Documents

admin.site.register(UserProfile)
admin.site.register(Documents)
