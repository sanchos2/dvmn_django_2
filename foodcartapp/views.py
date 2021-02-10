from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import Order, OrderItem, Product


def banners_list_api(request):  # noqa: D103
    # FIXME move data to db?
    return JsonResponse([  # noqa: WPS317
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        },
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


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
def register_order(request):  # noqa: D103, WPS212
    try:
        serialized_order = request.data
    except ValueError:
        return Response({'error': 'data not recognized'}, status=status.HTTP_400_BAD_REQUEST)

    if 'products' not in serialized_order:
        return Response({'error': 'Products list is missing'}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(serialized_order['products'], list):
        return Response({'error': 'Products not presented or not list'}, status=status.HTTP_400_BAD_REQUEST)
    if not serialized_order['products']:
        return Response({'error': 'Products list is empty'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        firstname=serialized_order['firstname'],
        lastname=serialized_order['lastname'],
        phonenumber=serialized_order['phonenumber'],
        address=serialized_order['address'],
    )

    for product in serialized_order['products']:
        if not isinstance(product['quantity'], int) and product['quantity'] < 0:
            return Response({'error': 'data not recognized'}, status=status.HTTP_400_BAD_REQUEST)
        OrderItem.objects.create(
            order=order,
            product_id=product['product'],
            quantity=product['quantity'],
        )
    return Response({'success': 'Order created successfully'}, status=status.HTTP_201_CREATED)
