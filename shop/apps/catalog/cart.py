from decimal import Decimal

from django.conf import settings
from django.http import QueryDict

from .models import Product


class Cart:
    """Цей клас реалізовує в собі взаємодію користувача з кошиком за допомогою

    Атрибути:
        request: запит користувача
        session: дані з сесії, які отримує з запиту
        cart:
    """
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(settings.BASKET_SESSION)

        if not cart:
            cart = self.session[settings.BASKET_SESSION] = {}

        self.cart = cart
        
    @property
    def get_data(self):
        """Отримуємо дані з запиту, який відправив на користувач на обробку кошика"""

        data = QueryDict(self.request.body)

        return data

    def save(self):
        """Зберігаємо оновлену сесію"""
        self.session.modified = True

    def add(self):
        """Додає нові дані в кошик з запиту POSt"""

        pk = self.request.POST.get('pk')
        product = Product.objects.get(pk=pk)
        cart = {}

        # Якщо цього товару ще нема в кошику, то додоає
        if pk not in self.cart.keys():
            cart = self.cart[pk] = {
                'poster': str(product.poster.url),
                'name': str(product.name),
                'price': float(product.price),
                'quantity': 1,
                'totalPrice': str(product.price)
                }
            self.save()

        return {'item': cart, 'id': pk, 'cartCounter': len(self.display())}

    def put(self):
        """Змінює дані з сесії про стан кошику"""

        pk = self.get_data.get('pk')
        quantity = int(self.get_data['quantity'])
        cart = {}

        if pk in self.cart.keys():
            cart = self.cart[pk]
            cart['quantity'] = quantity
            price = cart['price']
            cart['totalPrice'] = str(Decimal(price * quantity).quantize(Decimal('1.00')))
            self.save()

        return cart

    def delete(self, pk=None):

        pk = self.get_data.get('pk') if not pk else pk

        if pk in self.cart.keys():
            del self.cart[pk]
            self.save()

    def display(self):
        return self.cart.copy()







