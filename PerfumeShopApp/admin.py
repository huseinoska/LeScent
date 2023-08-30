from django.contrib import admin
from .models import Category, Product, Cart, CartItem

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)
    list_filter = ('category',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id',)
    filter_horizontal = ('products',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity',)
    list_filter = ('cart', 'product',)



