from django.contrib import admin
from .models import Category,Fooditem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','vendor','created_at','modified_at']
    prepopulated_fields = {'slug':('category_name',)}
    search_fields = ['category_name','vendor__vendor_name']

class FooditemAdmin(admin.ModelAdmin):
    list_display = ['food_title','category','price','vendor','created_at','modified_at']
    prepopulated_fields = {'slug':('food_title',)}    
    search_fields=['food_title','category__category_name','vendor__vendor_name','price']
    list_filter=['is_available']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Fooditem,FooditemAdmin)