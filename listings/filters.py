from rest_framework import filters

from .utils import longitude_nearby_locations_range, latitude_nearby_locations_range


class ListingsFreeDateFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        free_from = request.query_params.get('free_from', None)
        free_to = request.query_params.get('free_to', None)

        if free_from is not None and free_to is not None:
            free_range = [free_from, free_to]

            # Unbooked listings are also free to book
            unbooked_queryset = queryset.filter(bookings=None)

            filtered_queryset = queryset.exclude(
                bookings__check_in__range=free_range
            ).exclude(
                bookings__check_out__range=free_range
            )

            queryset = filtered_queryset | unbooked_queryset

        return queryset


class NearbyListingsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        longitude = request.query_params.get('near_long', None)
        latitude = request.query_params.get('near_lat', None)

        if longitude is not None and latitude is not None:
            longitude_range = longitude_nearby_locations_range(longitude)
            latitude_range = latitude_nearby_locations_range(latitude)

            queryset = queryset.filter(
                location__longitude__range=longitude_range,
                location__latitude__range=latitude_range
            )[:5]

        return queryset
