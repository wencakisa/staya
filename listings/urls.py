from django.urls import path, include

from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from listings.views import ListingViewSet, BookingViewSet, ReviewViewSet


listings_router = routers.SimpleRouter()
listings_router.register('listings', ListingViewSet)

bookings_router = nested_routers.NestedSimpleRouter(listings_router, 'listings', lookup='listing')
bookings_router.register('bookings', BookingViewSet, base_name='listing-bookings')

reviews_router = nested_routers.NestedSimpleRouter(listings_router, 'listings', lookup='listing')
reviews_router.register('reviews', ReviewViewSet, base_name='listing-reviews')

urlpatterns = [
    path('', include(listings_router.urls), name='listings'),
    path('', include(bookings_router.urls), name='listing-bookings'),
    path('', include(reviews_router.urls), name='listing-reviews'),
]
