# Generated by Django 3.0.7 on 2021-03-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_auto_20210315_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='slug',
            field=models.SlugField(default='banner1', max_length=40, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
