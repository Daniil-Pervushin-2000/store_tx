from django.contrib import admin
from .models import Order, City, Region, SaveOrder, SaveOrderProduct, OrderProduct, Customer

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Customer)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(SaveOrder)
admin.site.register(SaveOrderProduct)