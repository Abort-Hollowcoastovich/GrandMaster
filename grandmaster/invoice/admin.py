from django.contrib import admin

from .models import PayAccount, Bill

admin.site.register(PayAccount)
admin.site.register(Bill)
