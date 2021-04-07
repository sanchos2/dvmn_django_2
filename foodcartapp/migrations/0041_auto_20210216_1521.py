# Generated by Django 3.0.7 on 2021-02-16 12:21

from django.db import migrations


class Migration(migrations.Migration):

    def copy_product_price_to_orderitem_price(apps, schema_editor):
        Product = apps.get_model('foodcartapp', 'Product')
        OrderItem = apps.get_model('foodcartapp', 'OrderItem')
        orderitem_set = OrderItem.objects.all()
        if orderitem_set.exists():
            for item in orderitem_set.iterator():
                product = Product.objects.get(id=item.product_id)
                item.price = product.price
                item.save()

    dependencies = [
        ('foodcartapp', '0040_auto_20210216_1512'),
    ]

    operations = [
        migrations.RunPython(copy_product_price_to_orderitem_price),
    ]
