from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True, default="")
    price_original = models.DecimalField(max_digits=6, decimal_places=2)
    price_discount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    @property
    def is_discounted(self):
        return (
            self.price_discount is not None
            and self.price_discount < self.price_original
        )

    @property
    def display_price(self):
        return self.price_discount if self.is_discounted else self.price_original

    @property
    def discount_percent(self):
        return round(
            100 * (self.price_original - self.price_discount) / self.price_original
        )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    def get_upload_path(self, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return f"products/{filename}"

    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name + " Image"
