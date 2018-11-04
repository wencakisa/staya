from rest_framework import filters

from .models import Listing


class ListingsFreeDateFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        free_from = request.query_params.get('free_from', None)
        free_to = request.query_params.get('free_to', None)

        if free_from is not None and free_to is not None:
            return Listing.unbooked_listings(queryset, free_from, free_to)

        return queryset


class NearbyListingsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        longitude = request.query_params.get('near_long', None)
        latitude = request.query_params.get('near_lat', None)

        if longitude is not None and latitude is not None:
            return Listing.nearby_listings(queryset, longitude, latitude)

        return queryset
