from django.urls import path

from foodcartapp.views import banners_list_api, product_list_api, register_order   # noqa:  I001

app_name = 'foodcartapp'

urlpatterns = [
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', register_order),
]
