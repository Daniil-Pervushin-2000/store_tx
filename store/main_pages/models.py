from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Categories(models.Model):
    # CharField -> текстовое поля, ограниченной длинны
    # max_length -> сколько символов может быть в строке
    # verbose_name -> меняем имя для админ панели
    name = models.CharField(max_length=200, verbose_name='Имя категории')

    def __str__(self):
        return self.name

    # мета класс нужен для изменения свойств определенного класса
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    quantity = models.IntegerField(default=0, verbose_name='Кол-во')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    # DecimalField -> позволяет настраивать дробные цифры, точнее их округления
    # max_digits -> сколько максимум будет цифр до точки
    # decimal_places -> сколько будет цифр после точки
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')
    # CASCADE -> удаляет продукт если, удалить бренд
    # PROTECT -> не позволит удалить бренд, пока есть продукты с таким брендом
    # SET_NULL -> позволит удалить бренд, продукты останется только поля бренд будет null
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='Бренд')
    # null -> позволяет делать поля пустым
    # blank -> позволяет делать поля не обязательным для заполнения
    # ForeignKey -> Одно ко многим
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    # ManyToManyField -> Многое ко многим
    tags = models.ManyToManyField('Tags', related_name='tags_product', verbose_name='Теги')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=255)

    # sub_info = models.OneToOneField('SubInfo', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('show_detail', kwargs={'slug_path': self.slug})

    def get_first_photo(self):
        image = self.product_image.all().first()
        if image is not None:
            return image.photo.url
        else:
            return 'https://upload.wikimedia.org/wikipedia/commons/9/9a/%D0%9D%D0%B5%D1%82_%D1%84%D0%BE%D1%82%D0%BE.png'

    def get_all_photo(self):
        try:
            list_image = self.product_image.all()[1:]
            if list_image:
                return list_image
            else:
                return 'not image'
        except:
            return 'not image'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'


class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя тега')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ProductGallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_image')
    photo = models.ImageField(upload_to='product/image/', blank=True, null=True, verbose_name='Фото')


class Comments(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class FavoriteProduct(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class ViewsProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_session = models.CharField(max_length=150)


class RatingProduct(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    number_rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.number_rating)