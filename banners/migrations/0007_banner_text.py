# Generated by Django 3.0.7 on 2021-03-15 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0006_auto_20210315_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='text',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
