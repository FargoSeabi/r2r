from django.contrib import admin
from .models import Entrepreneur, Product, Order


@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'village', 'monthly_income', 'is_verified', 'is_active']
    list_filter = ['village', 'is_verified', 'is_active']
    search_fields = ['name', 'email', 'location', 'biography']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'entrepreneur', 'category', 'price', 'is_experience', 'availability', 'is_active']
    list_filter = ['category', 'is_experience', 'is_active', 'entrepreneur__village']
    search_fields = ['name', 'description', 'entrepreneur__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['id', 'created_at', 'updated_at']