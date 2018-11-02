from rest_framework import filters


class ListingsFreeDateFilterBackends(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        free_from = request.query_params.get('free_from', None)
        free_to = request.query_params.get('free_to', None)

        if free_from is not None and free_to is not None:
            free_range = [free_from, free_to]

            queryset = queryset.exclude(
                bookings__check_in__range=free_range
            ).exclude(
                bookings__check_out__range=free_range
            )

        return queryset
