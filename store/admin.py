from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('safe_name', 'slug')
    
    # دالة مساعدة لعرض الاسم في لوحة التحكم بشكل صحيح مع parler
    def safe_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    safe_name.short_description = "Category Name"

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('safe_title', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')

    def safe_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    safe_title.short_description = "Product Title"