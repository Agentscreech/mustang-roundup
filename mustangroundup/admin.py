from django.contrib import admin

# Register your models here.
from .models import Car, Category, Poll

admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Poll)