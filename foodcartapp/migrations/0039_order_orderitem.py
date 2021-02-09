# Generated by Django 3.0.7 on 2021-02-09 11:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20210209_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='Имя')),
                ('lastname', models.CharField(blank=True, max_length=50, verbose_name='Фамилия')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('address', models.TextField(verbose_name='Адрес доставки')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата/время заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foodcartapp.Order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foodcartapp.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказа',
            },
        ),
    ]
