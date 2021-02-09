from django.core.validators import MinValueValidator
from django.db import models


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
