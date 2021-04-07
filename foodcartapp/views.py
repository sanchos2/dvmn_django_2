from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from banners.models import Banner
from foodcartapp.models import Order, OrderItem, Product
from foodcartapp.serializers import OrderSerializer


def banners_list_api(request):  # noqa: D103
    banners = Banner.objects.all()
    dumped_banners = [
        {
            'title': banner.name,
            'src': banner.picture.url,
            'text': banner.text,
        } for banner in banners
    ]
    return JsonResponse(dumped_banners, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def product_list_api(request):  # noqa: D103
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            },
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
@transaction.atomic
def manage_order(request, pk=None):  # noqa: D103, WPS212
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = Order.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
        address=serializer.validated_data['address'],
    )
    products_fields = serializer.validated_data['products']
    products = [OrderItem(
        order=order,
        price=fields['product'].price,
        **fields,
    ) for fields in products_fields
    ]
    OrderItem.objects.bulk_create(products)
    return Response(OrderSerializer(instance=order).data, status=status.HTTP_201_CREATED)
