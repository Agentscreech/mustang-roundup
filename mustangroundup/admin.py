from django.contrib import admin

# Register your models here.
from .models import Car, Category, Poll, Division, Show_public

admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Poll)
admin.site.register(Division)
admin.site.register(Show_public)