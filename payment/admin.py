from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class OrderItemAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)