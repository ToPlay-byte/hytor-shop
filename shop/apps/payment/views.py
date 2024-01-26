from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse

import paypalrestsdk

from apps.catalog.cart import Cart
from .models import *
from .forms import OrderForm

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})


class OrderView(FormView):

    template_name = 'payment/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('payment:payment')

    def get(self, request, *args, **kwargs):
        get_object_or_404(Product, pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):

        cart = Cart(self.request)
        product = Product.objects.get(pk=self.kwargs['pk'])
        data = self.get_cart(cart)
        user = None

        if self.request.user.is_authenticated:
            user = self.request.user

        self.order = Order.objects.create(
            user=user, quantity=data.get('quantity'), product=product,
            total_price=data.get('totalPrice'), **form.cleaned_data,
        )

        cart.delete(pk=self.kwargs['pk'])

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('payment:payment', kwargs={'pk': self.order.pk})

    def get_cart(self, cart):

        data = cart.display().get(self.kwargs['pk'])

        if data:
            return data

        product = Product.objects.get(pk=int(self.kwargs['pk']))
        data = {
            'totalPrice': product.price,
            'quantity': 1,
        }
        return data


class PaymentView(View):
    """Цей класс представлення сторінку для оплати"""

    def get(self, request, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'), paid=False)
        return render(request, 'payment/checkout.html', {'pk': order.pk})


class SuccessView(TemplateView):
    """Цей клас представлення відповідає за відображення сторінки після успішного оформлення заказу"""

    template_name = 'payment/success.html'


class FailedView(TemplateView):
    """Цей класс представлення відповідає за сторінку, якщо було невірно оформлено замовлення"""

    template_name = 'payment/failed.html'


class OrdersList(ListView, LoginRequiredMixin):
    """Цей класс представлення відповідає за відображення сторінки з замовленнями користувача"""

    template_name = 'payment/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('paid')


class AjaxDeleteOrderView(View):
    """Цей класс надає видаляти замовлення за допомогою запиту ajax"""

    def post(self, request):

        pk = request.POST['pk']
        Order.objects.get(Q(user=request.user) & Q(pk=pk)).delete()

        return HttpResponse()


def create_order(request, pk):
    """Ця функція відповідає створює замовлення"""

    order = Order.objects.get(pk=pk)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment:execute', kwargs={'pk': order.pk})),
            "cancel_url": request.build_absolute_uri(reverse('payment:failed')),
        },
        "transactions": [
            {
                'item_list': {
                    'items': [{
                        'name': order.product.name,
                        'price': order.product.price,
                        'quantity': order.quantity,
                        'currency': 'USD'
                    }]
                },
                "amount": {
                    "total": str(order.total_price),
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
        "note_to_payer": order.pk
    })

    if payment.create():
        return redirect(payment.links[1].href)

    return render(request, 'payment/failed.html')


def execute_payment(request, pk):
    """Ця функція обробляє замовлення"""

    order = Order.objects.get(pk=pk)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        order.paid = True
        order.save()
        return render(request, 'payment/success.html')

    return render(request, 'payment/failed.html')
