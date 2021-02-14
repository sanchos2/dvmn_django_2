from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from foodcartapp.models import Order, Product, Restaurant


class Login(forms.Form):  # noqa: D101
    username = forms.CharField(  # noqa: WPS317
        label='Логин', max_length=75, required=True,  # noqa: WPS432
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя',
        }),
    )
    password = forms.CharField(  # noqa: WPS317
        label='Пароль', max_length=75, required=True,  # noqa: WPS432
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
    )


class LoginView(View):  # noqa: D101
    def get(self, request, *args, **kwargs):  # noqa: D102
        form = Login()
        return render(request, 'login.html', context={
            'form': form,
        })

    def post(self, request):  # noqa: D102
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect('restaurateur:RestaurantView')
                return redirect('start_page')

        return render(request, 'login.html', context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):  # noqa: D101
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):  # noqa: D103
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):  # noqa: D103
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},  # noqa: WPS110
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability),
        )

    return render(request, template_name='products_list.html', context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):  # noqa: D103
    return render(request, template_name='restaurants_list.html', context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):  # noqa: D103
    orders = Order.objects.all()
    return render(request, template_name='order_items.html', context={'orders': orders})
