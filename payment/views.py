import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from basket.basket import Basket


@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = settings.STRIP_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='brl',
        metadata={'userid': request.user.id}
    )
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'
