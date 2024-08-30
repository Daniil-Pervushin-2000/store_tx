from django.urls import path
from . import views

urlpatterns = [
    # path(запрос, функция которая отвечает за шаблон, указываем имя url адреса)
    path('', views.index_view, name='index_path'),
    path('product/detail/<slug:slug_path>/', views.ShowDetailView.as_view(), name='show_detail'),
    path('product/shop/', views.ShopView.as_view(), name='shop_path'),
    path('product/shop/category/<int:cat_id>/', views.ShowCategoryView.as_view(), name='show_category'),
    path('product/shop/brand/<str:brand_name>/', views.ShowBrandView.as_view(), name='show_brand'),
    path('product/comment/<int:pk_product>/', views.comment_logic, name='comment_activate'),
    path('product/favorite/<int:pk_product>/', views.favorite_logic, name='favorite_activate'),
    path('product/search/', views.search_logic, name='search_activate'),
    path('product/rating/<int:pk_product>/', views.rating_logic, name='rating_activate'),
    path('product/create/', views.create_product_logic, name='create_product'),

    path('product/my/favorite/<int:user_id>/', views.show_favorite_view, name='show_favorite_path')
]
