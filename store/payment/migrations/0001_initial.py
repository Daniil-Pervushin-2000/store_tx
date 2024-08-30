# Generated by Django 4.2.14 on 2024-08-23 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_pages', '0006_viewsproduct_ratingproduct_favoriteproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=250, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=250, verbose_name='Имя покупателя')),
                ('last_name', models.CharField(default='', max_length=250, verbose_name='Фамилия покупателя')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата заказа')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Заказ выполнен')),
                ('shipping', models.BooleanField(default=True, verbose_name='Доставка')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=250, verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='SaveOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата заказа')),
                ('total_price', models.FloatField(default=0, verbose_name='Сумма заказа')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'История заказа',
                'verbose_name_plural': 'История заказов',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300, verbose_name='Адрес (ул, дом, кв)')),
                ('phone', models.CharField(max_length=250, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата доставки')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.city', verbose_name='Город')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.customer', verbose_name='Покупатель')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.order', verbose_name='Заказ')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Адрес доставки',
                'verbose_name_plural': 'Адреса доставки',
            },
        ),
        migrations.CreateModel(
            name='SaveOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=250, verbose_name='Продукт')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('product_price', models.FloatField(verbose_name='Цена продукта')),
                ('final_price', models.FloatField(verbose_name='На сумму')),
                ('added_at', models.DateTimeField(auto_now=True, verbose_name='Дата покупки')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='payment.saveorder')),
            ],
            options={
                'verbose_name': 'История заказанного продукта',
                'verbose_name_plural': 'История заказанных продуктов',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество')),
                ('added_at', models.DateTimeField(auto_now=True, verbose_name='Дата добавления')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_pages.products', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Продукт в заказе',
                'verbose_name_plural': 'Продукты в заказе',
            },
        ),
    ]
