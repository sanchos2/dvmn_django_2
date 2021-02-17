from django.conf import settings
from django.contrib import admin
from django.shortcuts import HttpResponseRedirect, reverse
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme

from foodcartapp.models import Product, ProductCategory  # noqa:  I001
from foodcartapp.models import Restaurant, RestaurantMenuItem  # noqa:  I001
from foodcartapp.models import Order, OrderItem  # noqa:  I001


class RestaurantMenuItemInline(admin.TabularInline):  # noqa: D101
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):  # noqa: D101
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline,
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ],
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide',
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:  # noqa: D106, WPS306, WPS431
        css = {
            'all': (
                static('admin/foodcartapp.css')
            ),
        }

    def get_image_preview(self, obj):  # noqa: D102, WPS110
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" height="200"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):  # noqa: D102, WPS110
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" height="50"/></a>',
            edit_url=edit_url,
            src=obj.image.url,
        )
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):  # noqa: D101, WPS440, F811
    pass  # noqa: WPS420, WPS604


class OrderItemInline(admin.TabularInline):  # noqa: D101
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):  # noqa: D101
    inlines = [OrderItemInline]
    list_display = ['firstname', 'phonenumber', 'status', 'created_at']
    fieldsets = (
        ('Заказ', {
            'fields': [
                'firstname',
                'lastname',
                'phonenumber',
                'address',
                'comment',
                'status',
                'created_at',
                'called_at',
                'delivered_at',
            ],
        }),
    )
    readonly_fields = ['created_at']

    def response_change(self, request, obj):  # noqa: WPS110
        """При переходе в админку из фронта редиректит обратно на фронт."""
        response = super().response_change(request, obj)
        if 'next' in request.GET and url_has_allowed_host_and_scheme(request.GET['next'], settings.ALLOWED_HOSTS):
            return HttpResponseRedirect(request.GET['next'])
        return response
