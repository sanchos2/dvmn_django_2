# Generated by Django 3.0.7 on 2021-03-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_order_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='адрес')),
                ('lat', models.FloatField(verbose_name='Широта', null=True)),
                ('lon', models.FloatField(verbose_name='Долгота', null=True)),
                ('fetch_at', models.DateTimeField(verbose_name='Координаты загружены', null=True)),
            ],
        ),
    ]