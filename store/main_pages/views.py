from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify

from account.models import Profile
from .models import Categories, Products, Brand, Tags, Comments, FavoriteProduct, ViewsProduct, RatingProduct
from .forms import CommentForm, CreateProductForm


def index_view(request):
    # конструкция которая забирает все продукты
    # Имя_таблицы.объекты.все
    products = Products.objects.all()

    # словаря, у которого мы в шаблоне будем обращаться к ключ, для получения QuerySet
    content = {
        'products': products,
        'title': 'Главная страница'
    }

    # render(запрос, путь к шаблону, словарь для отдачи данных в шаблон)
    return render(request, 'pages/index.html', context=content)


# def show_detail_view(request, slug_path):
#     # get -> забирает из БД один объект, по условию
#     product = Products.objects.get(slug=slug_path)
#     comments = Comments.objects.filter(product=product)
#
#     if request.method == 'POST':
#         form_comment = CommentForm(data=request.POST)
#         if form_comment.is_valid():
#             form_comment = form_comment.save(commit=False)
#             form_comment.auth = request.user
#             form_comment.product = product
#             form_comment.save()
#             return redirect('show_detail', slug_path)
#     else:
#         form_comment = CommentForm()
#
#     if request.user.is_authenticated:
#         if not request.session.session_key:
#             request.session.save()
#
#         session_key = request.session.session_key
#         status_view = ViewsProduct.objects.filter(product=product, user_session=session_key).exists()
#         if status_view is False and session_key != 'None':
#             view = ViewsProduct()
#             view.product = product
#             view.user_session = session_key
#             view.save()
#
#             product.views += 1
#             product.save()
#
#     content = {
#         'product': product,
#         'title': f'Продукт {product.title}',
#         'form_comment': form_comment,
#         'comments': comments,
#         'rating_range': [n for n in range(1, 5+1)]
#     }
#     return render(request, 'pages/detail.html', content)
#
#
# def shop_view(request):
#     brands = Brand.objects.all()
#     categories = Categories.objects.all()
#
#     products = Products.objects.all()
#     # Paginator -> класс для создания пагинации, в него мы указываем QuerySet, и какое
#     # количество должнобыть на страницы
#     paginator = Paginator(products, 2)
#     page = request.GET.get('page')
#     result = paginator.get_page(page)
#
#     context = {
#         'title': 'Все товары STORE TX',
#         'categories': categories,
#         'brands': brands,
#         'products': result
#     }
#     return render(request, 'pages/shop.html', context)
#
#
# def show_category_view(request, cat_id):
#     brands = Brand.objects.all()
#
#     categories = Categories.objects.all()
#     category = Categories.objects.get(pk=cat_id)
#     # filter -> забирает все объекты который подходят под условия
#     products = Products.objects.filter(category_id=cat_id)
#
#     context = {
#         'title': f'Категория товара: {category.name}',
#         'categories': categories,
#         'brands': brands,
#         'products': products
#     }
#     return render(request, 'pages/shop.html', context)
#
#
# def show_brand_view(request, brand_name):
#     categories = Categories.objects.all()
#
#     brands = Brand.objects.all()
#     brand = Brand.objects.get(name=brand_name)
#     # filter -> забирает все объекты который подходят под условия
#     products = Products.objects.filter(brand_id=brand.pk)
#
#     context = {
#         'title': f'Бренд товара: {brand.name}',
#         'categories': categories,
#         'brands': brands,
#         'products': products
#     }
#     return render(request, 'pages/shop.html', context)


class ShowDetailView(DetailView):
    model = Products
    context_object_name = 'product'
    slug_url_kwarg = 'slug_path'
    template_name = 'pages/detail.html'

    extra_context = {
        'form_comment': CommentForm,
        'rating_range': [n for n in range(1, 5 + 1)]
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Products.objects.get(slug=self.kwargs['slug_path'])
        if self.request.user.is_authenticated:
            if not self.request.session.session_key:
                self.request.session.save()

            session_key = self.request.session.session_key
            status_view = ViewsProduct.objects.filter(product=product, user_session=session_key).exists()
            if status_view is False and session_key != 'None':
                view = ViewsProduct()
                view.product = product
                view.user_session = session_key
                view.save()

                product.views += 1
                product.save()
        context['title'] = f'Продукт {product.title}',
        context['comments'] = Comments.objects.filter(product=product)
        return context


class ShopView(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'pages/shop.html'
    paginate_by = 2

    extra_context = {
        'title': 'Все товары STORE TX',
        'brands': Brand.objects.all(),
        'categories': Categories.objects.all()
    }


class ShowCategoryView(ShopView):
    def get_queryset(self):
        category = Categories.objects.get(pk=self.kwargs['cat_id'])
        return category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Categories.objects.get(pk=self.kwargs['cat_id'])
        context['title'] = f'Категория товара: {category.name}'
        return context


class ShowBrandView(ShopView):
    def get_queryset(self):
        brand = Brand.objects.get(name=self.kwargs['brand_name'])
        return brand

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        brand = Brand.objects.get(name=self.kwargs['brand_name'])
        context['title'] = f'Бренд товара: {brand.name}'
        return context


def comment_logic(request, pk_product):
    product = Products.objects.get(pk=pk_product)

    if request.method == 'POST':
        form_comment = CommentForm(data=request.POST)
        if form_comment.is_valid():
            form_comment = form_comment.save(commit=False)
            form_comment.auth = request.user
            form_comment.product = product
            form_comment.save()
            return redirect('show_detail', product.slug)


def favorite_logic(request, pk_product):
    product = get_object_or_404(Products, pk=pk_product)
    user = request.user
    status_favorite = FavoriteProduct.objects.filter(auth=user, product_id=pk_product).exists()
    if status_favorite is True:
        favorite = FavoriteProduct.objects.get(auth=user, product_id=pk_product)
        favorite.delete()
    else:
        favorite = FavoriteProduct.objects.create(auth=user, product_id=pk_product)
        favorite.save()

    return redirect(request.META.get('HTTP_REFERER', 'index_path'))


def search_logic(request):
    brands = Brand.objects.all()
    categories = Categories.objects.all()
    query = request.GET.get('q')
    products = Products.objects.filter(
        Q(title__iregex=query) | Q(title__icontains=query)
    )
    content = {
        'title': f'Результат поиска: {query}',
        'categories': categories,
        'brands': brands,
        'products': products
    }
    return render(request, 'pages/shop.html', context=content)


def rating_logic(request, pk_product):
    auth = request.user
    product = get_object_or_404(Products, pk=pk_product)
    status = RatingProduct.objects.filter(auth=auth, product_id=pk_product).exists()
    if status is False:
        if request.method == 'POST':
            number_rating = request.POST.get('rating')
            rating = RatingProduct.objects.create(auth=auth, product=product, number_rating=number_rating)
            rating.save()
            return redirect('show_detail', product.slug)


def create_product_logic(request):
    if request.method == 'POST':
        form = CreateProductForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            price = form.cleaned_data.get('price')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            brand = form.cleaned_data.get('brand')
            slug = slugify(title)
            product = Products.objects.create(title=title, price=price, description=description,
                                              category=category, brand=brand, slug=slug)

            product.save()
            return redirect('index_path')
    else:
        form = CreateProductForm()

    context = {
        'form': form
    }
    return render(request, 'pages/create_product.html', context)


def show_favorite_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    products = FavoriteProduct.objects.filter(auth=profile.user)
    comment = Comments.objects.filter(auth=profile.user)
    content = {
        'profile': profile,
        'count_user_comment': comment.count(),
        'products': products
    }
    return render(request, 'pages/favorite.html', content)




# TODO: 6 блок
# TODO: Работа с профилем создание изменения :
# TODO: Создание продукта через формы / изменения / удаления :
# TODO: Реализация оплаты :




