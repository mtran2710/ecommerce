from core.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key', None)
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        cart_products = []
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for id in product_ids:
            product = products.get(id=id)
            cart_products.append({
                'product': product,
                'quantity': self.cart[id]['quantity']
            })
        return cart_products
    
    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for product in products:
            total += self.cart[str(product.id)]['quantity'] * product.display_price
        return total