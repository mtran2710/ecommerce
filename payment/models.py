from django.db import models
from core.models import Product, Customer
from django.db.models.signals import post_save

# Create your models here.
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_address = models.CharField(max_length=1000)
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f"Shipping Address - {self.id}"
    
#Create a user Shipping Address when a customer is created
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        shipping_address = ShippingAddress(customer=instance)
        shipping_address.save()
        
post_save.connect(create_shipping_address, sender=Customer)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return (
            f"Order {self.id} by {self.customer.first_name} {self.customer.last_name}"
        )


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order Item - {self.id}"