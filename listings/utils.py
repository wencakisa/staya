import numpy

from .models import Location


def get_nearby_locations_in_radius(coordinate, diff):
    return sorted(numpy.linspace(coordinate - diff, coordinate + diff, num=2).tolist())


def longitude_nearby_locations_range(longitude):
    return get_nearby_locations_in_radius(float(longitude), Location.NEARBY_KM_LONG)


def latitude_nearby_locations_range(latitude):
    return get_nearby_locations_in_radius(float(latitude), Location.NEARBY_KM_LAT)
