from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import get_object_or_404

from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .permissions import (
    ListingCreatingPermission,
    ListingModifyingPermission,
    ListingBookingPermission,
    ListingReviewPermission
)
from .filters import ListingsFreeDateFilterBackends


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = (
        # Listings should be availbable for anonymous users too
        IsAuthenticatedOrReadOnly,
        ListingCreatingPermission,
        ListingModifyingPermission,
    )
    filter_backends = (ListingsFreeDateFilterBackends,)

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user)


class BaseNestedListingResourceViewSet(viewsets.ModelViewSet):
    model_class = None

    def get_queryset(self):
        return self.model_class.objects.filter(listing=self.kwargs['listing_pk'])

    def perform_create(self, serializer):
        user = self.request.user
        listings = Listing.objects.all()

        listing = get_object_or_404(listings, id=self.kwargs['listing_pk'])

        self.check_object_permissions(self.request, listing)

        serializer.save(user=user, listing=listing)


class BookingViewSet(BaseNestedListingResourceViewSet):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, ListingBookingPermission)
    model_class = Booking


class ReviewViewSet(BaseNestedListingResourceViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, ListingReviewPermission)
    model_class = Review
