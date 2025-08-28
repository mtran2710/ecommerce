from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
import json

from .cart import Cart
from core.models import Product

# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    total = cart.get_total()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'cart/cart_item_details.html',
            {
                'cart_products': cart_products,
                'total': total
            }
        )
        return JsonResponse({'html': html, 'cart_count': len(cart)})
    return render(request, 'cart/cart_detail.html')

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        quantity = int(data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        quantity = int(data.get('quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity, update_quantity=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})