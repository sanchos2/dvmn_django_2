from django.http import JsonResponse
from django.templatetags.static import static
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
def register_order(request):  # noqa: D103
    try:
        serialized_order = request.data
    except ValueError:
        return Response({'error': 'data not recognized'})
    order = Order.objects.create(
        firstname=serialized_order['firstname'],
        lastname=serialized_order['lastname'],
        phonenumber=serialized_order['phonenumber'],
        address=serialized_order['address'],
    )
    for product in serialized_order['products']:
        OrderItem.objects.create(
            order=order,
            product_id=product['product'],
            quantity=product['quantity'],
        )
    return Response({'success': 'Order created successfully'})
