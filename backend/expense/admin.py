from django.contrib import admin
from .models import UserDeatil, Expense
#from .models import *  another way :

# Register your models here.
admin.site.register(UserDeatil)
admin.site.register(Expense)

