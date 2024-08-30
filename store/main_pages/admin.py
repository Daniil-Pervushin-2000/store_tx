from django.contrib import admin
from .models import Categories, Products, Brand, Tags, ProductGallery


# простое подключения, минус его в том что нельзя настроить админ панель, плюс его легко подключить
admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Tags)


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    # указываем какие поля показывать у продукта
    list_display = ['pk', 'title', 'price', 'category', 'brand']
    # указываем по каким полям можно переходить на сам продукт
    list_display_links = ('pk', 'title')
    # позволяет нам искать продукты по title
    search_fields = ['title']
    # само будет заполнять поля slug по title
    prepopulated_fields = {'slug': ['title']}
    # позволяет нам изменять указанное поле
    list_editable = ['category']
    # позволяет нам подключать классы TabularInline
    inlines = [ProductGalleryInline]
    ordering = ['pk']
    list_per_page = 2

    field = ['___all___']

    filter_horizontal = ['tags']

