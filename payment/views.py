from django.shortcuts import render

from core.models import Customer
from .forms import ShippingAddressForm
from .models import ShippingAddress
# Create your views here.
def payment_success(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            if request.user.is_authenticated:
                customer = Customer.objects.get(user_id=request.user.id)
                shipping_address.customer = customer
            shipping_address.save()
    return render(request, "payment/payment_success.html")

def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user_id=request.user.id)
        shipping_user = ShippingAddress.objects.filter(customer_id=customer.id).order_by('-id').first()
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"shipping_form": shipping_form})
    else:
        shipping_form = ShippingAddressForm(request.POST or None)
        return render(request, "payment/checkout.html", {"shipping_form": shipping_form})