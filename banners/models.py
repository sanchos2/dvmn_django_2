from django.db import models


class Banner(models.Model):  # noqa: D101

    name = models.CharField('Название', max_length=150)  # noqa: WPS432
    picture = models.ImageField('Баннер')
    slug = models.SlugField('URL', max_length=40, unique=True)  # noqa: WPS432
    order = models.PositiveIntegerField('Сортировка', default=0, blank=False, null=False)
    text = models.TextField('Описание', blank=True)

    class Meta:  # noqa: D106, WPS306
        ordering = ['order']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):  # noqa: D105
        return self.name

    def get_absolute_url(self):  # noqa: D102
        return self.picture.url
