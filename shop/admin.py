from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    pass