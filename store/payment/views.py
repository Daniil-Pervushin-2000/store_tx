import stripe

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .models import Customer, SaveOrder, SaveOrderProduct
from .utils import CartForAuthenticated, get_cart_data
from .forms import CustomerForm, ShippingForm


def cart(request):
    cart_info = get_cart_data(request)
    content = {
        'title': 'Моя корзина',
        'order': cart_info['order'],
        'products': cart_info['products'],
        'len_products': len(cart_info['products'], )
    }
    return render(request, 'payment/cart.html', content)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticated(request, product_id, action)
        return redirect(request.META.get('HTTP_REFERER', 'index_path'))
    else:
        return redirect(request.META.get('HTTP_REFERER', 'index_path'))


def clear_cart(request):
    user_cart = CartForAuthenticated(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product

        product.quantity += quantity
        product.save()

        order_product.delete()
    return redirect('cart_path')


def checkout(request):
    if request.user.is_authenticated:
        card_info = get_cart_data(request)

        content = {
            'title': 'Оформление заказа',
            'order': card_info['order'],
            'products': card_info['products'],

            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm()
        }

        return render(request, 'payment/checkout.html', content)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticated(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data.get('first_name')
            customer.last_name = customer_form.cleaned_data.get('last_name')
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.customer = Customer.objects.get(user=request.user)
            shipping.order = user_cart.get_cart_info()['order']
            shipping.save()

        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': "Покупки на сайте STORE TX"
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success_path')),
            cancel_url=request.build_absolute_uri(reverse('checkout_activate'))
        )

        return redirect(session.url, 303)


def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticated(request)
        cart_info = user_cart.get_cart_info()
        order = cart_info['order']

        order.is_completed = True
        order.save()

        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price)
        order_save.save()

        order_products = order.orderproduct_set.all()
        for item in order_products:
            save_order_product = SaveOrderProduct.objects.create(
                order_id=order_save.pk,
                product=str(item),
                quantity=item.quantity,
                product_price=item.product.price,
                final_price=item.get_total_price,
            )
            save_order_product.save()

        user_cart.clear_cart()
        return render(request, 'payment/success.html')
