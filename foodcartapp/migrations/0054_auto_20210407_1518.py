# Generated by Django 3.0.7 on 2021-04-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_auto_20210407_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='fetch_at',
        ),
        migrations.AddField(
            model_name='place',
            name='fetched_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Координаты загружены'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lon',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота'),
        ),
    ]
