from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'category', 'price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'status']
