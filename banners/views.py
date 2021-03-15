from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from banners.models import Banner


def get_banners(request):  # noqa: D103
    banners = Banner.objects.values('slug')
    return JsonResponse({'banners': list(banners)})


def get_banner_url(request, slug):  # noqa: D103
    picture = get_object_or_404(Banner, slug=slug)
    return redirect(picture)
