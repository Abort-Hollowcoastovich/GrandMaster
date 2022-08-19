from django.contrib import admin

from .models import PayAccount, Bill, UserBill

admin.site.register(PayAccount)
admin.site.register(Bill)
admin.site.register(UserBill)
