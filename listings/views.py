from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Amenity, Listing, Booking, Review
from .serializers import (
    AmenitySerializer,
    ListingSerializer,
    BookingSerializer,
    ReviewSerializer
)
from .permissions import (
    IsResidentUser,
    ListingCreatingPermission,
    ListingModifyingPermission,
    ListingBookingPermission,
    ListingReviewPermission
)
from .filters import ListingsFreeDateFilter, NearbyListingsFilter


class AmenitiesList(generics.ListAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()
    permission_classes = (IsAuthenticated, IsResidentUser)


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = (
        # Listings should be availbable for anonymous users too
        IsAuthenticatedOrReadOnly,
        ListingCreatingPermission,
        ListingModifyingPermission
    )
    filter_backends = (filters.SearchFilter, NearbyListingsFilter, ListingsFreeDateFilter)
    search_fields = ('title', 'guest_amount', 'location__title', 'resident__username')

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, ListingBookingPermission)

    def get_queryset(self):
        return Booking.current_bookings().filter(listing=self.kwargs['listing_pk'])

    def perform_create(self, serializer):
        user = self.request.user
        listings = Listing.objects.all()

        listing = generics.get_object_or_404(listings, id=self.kwargs['listing_pk'])

        self.check_object_permissions(self.request, listing)

        serializer.save(user=user, listing=listing)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, ListingReviewPermission)

    def get_queryset(self):
        return Review.objects.filter(listing=self.kwargs['listing_pk'])

    def perform_create(self, serializer):
        user = self.request.user
        listings = Listing.objects.all()

        listing = generics.get_object_or_404(listings, id=self.kwargs['listing_pk'])

        self.check_object_permissions(self.request, listing)

        serializer.save(user=user, listing=listing)
