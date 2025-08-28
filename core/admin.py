from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Customer, Product, ProductImage

# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 3
    fields = ["image", "image_preview", "uploaded_at"]
    readonly_fields = ["uploaded_at", "image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return ""

    image_preview.short_description = "Preview"
    
    def has_add_permission(self, request, obj=None):
        if obj and obj.images.count() >= 3:
            return False
        return True
        
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            remaining_slots = 3 - obj.images.count()
            formset.help_text = f"Maximum 3 images per product. {remaining_slots} slot(s) remaining."
        return formset


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["name", "stock"]

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
