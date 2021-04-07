import requests
from django.conf import settings
from django.utils import timezone
from requests import exceptions

from foodcartapp.models import Place


def fetch_coordinates(apikey, place):
    """Полученает координаты по адресу."""
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': place, 'apikey': apikey, 'format': 'json'}  # noqa: WPS110
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat, lon


def add_coordinates(place):
    """Добавляет координаты к объекту."""
    try:
        place.lat, place.lon = fetch_coordinates(settings.GEO_API_KEY, place.address)  # noqa: WPS414
    except (exceptions.HTTPError, IndexError):
        place.lat, place.lon = None, None  # noqa: WPS414
    place.fetched_at = timezone.now()
    place.save()


def return_place(address):
    """Возвращает объект Place c требуемым адресом"""
    place, created = Place.objects.get_or_create(address=address)
    if created:
        add_coordinates(place)
    return place
