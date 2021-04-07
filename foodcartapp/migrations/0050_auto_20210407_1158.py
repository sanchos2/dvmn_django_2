# Generated by Django 3.0.7 on 2021-04-07 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_auto_20210304_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Необработанный', 'Unprocessed'), ('Обработанный', 'Processed')], default='Необработанный', max_length=14, verbose_name='Статус'),
        ),
    ]
