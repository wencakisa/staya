from django.urls import path, include

from rest_framework import routers

from listings.views import ListingViewSet


listings_router = routers.SimpleRouter()
listings_router.register('listings', ListingViewSet)

urlpatterns = [
    path('', include(listings_router.urls), name='listings'),
]
