from django.contrib import admin
from .models import Category, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'title', 'price']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
