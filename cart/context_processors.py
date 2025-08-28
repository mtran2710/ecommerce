from .cart import Cart

def cart(request):
    """
    This allows us to access the cart in all pages.
    """
    cart = Cart(request)
    return {'cart': cart, 'cart_products': cart.get_products(), 'total': cart.get_total()}