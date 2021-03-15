# Generated by Django 3.0.7 on 2021-03-15 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0005_auto_20210315_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='banner',
            name='slug',
            field=models.SlugField(max_length=40, unique=True, verbose_name='URL'),
        ),
    ]
