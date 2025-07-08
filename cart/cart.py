from decimal import Decimal
from django.conf import settings
from django.core.cache import cache
from products.models import Product, Size

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self._load_cart_data()
        
    def _load_cart_data(self):
        cart = self.session.get(settings.CART_SESSION_ID, {})
        return cart if isinstance(cart, dict) else {}

    def add(self, product, size=None, quantity=1, override_quantity=False):
        key = self._generate_key(product.id, size)
        
        if key not in self.cart:
            self.cart[key] = self._new_cart_item(product, size)
        
        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
            
        self._clean_quantity(key)
        self.save()

    def _generate_key(self, product_id, size):
        if size is None:
            return str(product_id)
        size_code = getattr(size, 'name', str(size))
        return f"{product_id}_{size_code}"

    def _new_cart_item(self, product, size):
        return {
            'quantity': 0,
            'price': str(product.get_current_price()),
            'size': str(getattr(size, 'name', size)) if size else None,
            'product_id': product.id,
            'size_id': getattr(size, 'id', None),
        }

    def _clean_quantity(self, key):
        if self.cart.get(key, {}).get('quantity', 1) <= 0:
            del self.cart[key]

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        cache.delete(f'cart_{self.session.session_key}')

    def remove(self, product, size=None):
        key = self._generate_key(product.id, size)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        product_ids = {item.get('product_id') for item in self.cart.values() if item.get('product_id')}
        
        # Get all size_ids that exist and are not None
        size_ids = {item.get('size_id') for item in self.cart.values() 
                   if item.get('size_id') is not None}
        
        products = Product.objects.filter(id__in=product_ids).in_bulk() if product_ids else {}
        sizes = Size.objects.filter(id__in=size_ids).in_bulk() if size_ids else {}
        
        for item in self.cart.values():
            product = products.get(item.get('product_id'))
            if not product:
                continue
                
            size_obj = sizes.get(item.get('size_id')) if item.get('size_id') else None
            
            yield {
                'product': product,
                'size': item.get('size'),
                'size_obj': size_obj,
                'quantity': item.get('quantity', 0),
                'price': Decimal(item.get('price', 0)),
                'total_price': Decimal(item.get('price', 0)) * item.get('quantity', 0),
                'product_id': item.get('product_id'),
                'key': self._generate_key(item.get('product_id'), item.get('size'))
            }

    def __len__(self):
        return sum(item.get('quantity', 0) for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item.get('price', 0)) * item.get('quantity', 0) 
            for item in self.cart.values()
        )

    def get_product_quantity(self, product, size=None):
        key = self._generate_key(product.id, size)
        return self.cart.get(key, {}).get('quantity', 0)
    
    def count(self):
        return sum(item.get('quantity', 0) for item in self.cart.values())
