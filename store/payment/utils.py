from .models import Products, Order, OrderProduct, Customer


class CartForAuthenticated:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created =Order.objects.get_or_create(customer=customer)
        order_product = order.orderproduct_set.all()

        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity

        return {
            'order': order,
            'products': order_product,
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity
        }


    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Products.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear_cart(self):
        order = self.get_cart_info()['order']
        order_product = order.orderproduct_set.all()
        for product in order_product:
            product.delete()

        order.save()


def get_cart_data(request):
    cart = CartForAuthenticated(request)
    cart_info = cart.get_cart_info()

    return {
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity']
    }