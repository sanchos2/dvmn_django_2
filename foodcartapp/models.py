from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum  # noqa: WPS347
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):  # noqa: D101
    name = models.CharField('название', max_length=50)  # noqa: WPS432
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)  # noqa: WPS432

    class Meta:  # noqa: D106, WPS306
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):  # noqa: D105
        return self.name


class ProductQuerySet(models.QuerySet):  # noqa: D101
    def available(self):  # noqa: D102
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):  # noqa: D101
    name = models.CharField('название', max_length=50)  # noqa: WPS432

    class Meta:  # noqa: D106, WPS306
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):  # noqa: D105
        return self.name


class Product(models.Model):  # noqa: D101
    name = models.CharField('название', max_length=50)  # noqa: WPS432
    category = models.ForeignKey(
        ProductCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        related_name='products',
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', blank=True)  # noqa: WPS432

    objects = ProductQuerySet.as_manager()  # noqa: WPS110

    class Meta:  # noqa: D106, WPS306
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):  # noqa: D105
        return self.name


class RestaurantMenuItem(models.Model):  # noqa: D101
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='ресторан',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    class Meta:  # noqa: D106, WPS306
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product'],
        ]

    def __str__(self):  # noqa: D105
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):
    """Расчет цены заказа."""

    def amount(self):  # noqa: D102
        return self.annotate(
            amount=Sum(
                F('order_items__product__price') * F('order_items__quantity'),
                output_field=models.DecimalField(),
            ),
        )


class Order(models.Model):
    """Заказ."""

    firstname = models.CharField('Имя', max_length=50)  # noqa: WPS432
    lastname = models.CharField('Фамилия', max_length=50, blank=True)  # noqa: WPS432
    phonenumber = PhoneNumberField('Телефон')
    address = models.TextField('Адрес доставки')
    order_date = models.DateTimeField('Дата/время заказа', auto_now_add=True)
    objects = OrderQuerySet.as_manager()  # noqa: WPS110

    class Meta:  # noqa: D106, WPS306

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):  # noqa: D105
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderItem(models.Model):
    """Позиция заказа."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField('Количество', validators=[MinValueValidator(1)])

    class Meta:  # noqa: D106, WPS306

        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):  # noqa: D105
        return f'{self.product} - {self.quantity}'
