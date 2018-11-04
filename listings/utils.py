from math import cos
import numpy

LAT_DEGREE_TO_KM = 110.574
LONG_DEGREE_TO_KM = 111.320 * cos(LAT_DEGREE_TO_KM)
NEARBY_KM_LAT = LAT_DEGREE_TO_KM * 0.005
NEARBY_KM_LONG = LONG_DEGREE_TO_KM * 0.005

def get_nearby_locations_in_radius(coordinate, diff):
    return sorted(numpy.linspace(coordinate - diff, coordinate + diff, num=2).tolist())


def longitude_nearby_locations_range(longitude):
    return get_nearby_locations_in_radius(float(longitude), NEARBY_KM_LONG)


def latitude_nearby_locations_range(latitude):
    return get_nearby_locations_in_radius(float(latitude), NEARBY_KM_LAT)
