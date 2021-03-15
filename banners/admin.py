from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from banners.models import Banner


@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):  # noqa: D101
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['order', 'name', 'slug']
