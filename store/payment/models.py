from django.db import models
from django.contrib.auth.models import User
from main_pages.models import Products


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    first_name = models.CharField(max_length=250, default='', verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=250, default='', verbose_name='Фамилия покупателя')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Заказ выполнен')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    address = models.CharField(max_length=300, verbose_name='Адрес (ул, дом, кв)')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    phone = models.CharField(max_length=250, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата доставки')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class City(models.Model):
    city = models.CharField(max_length=250, verbose_name='Город')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Region(models.Model):
    region = models.CharField(max_length=250, verbose_name='Регион')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма заказа')

    def __str__(self):
        return f'Номер заказа №{self.pk}'

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'История заказов'


class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='order_products')
    product = models.CharField(max_length=250, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена продукта')
    final_price = models.FloatField(verbose_name='На сумму')
    added_at = models.DateTimeField(auto_now=True, verbose_name='Дата покупки')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'История заказанного продукта'
        verbose_name_plural = 'История заказанных продуктов'