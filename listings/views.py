from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Listing
from .serializers import ListingSerializer
from .permissions import ListingCreatingPermission, ListingModifyingPermission


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = (
        # Listings should be availbable for anonymous users too
        IsAuthenticatedOrReadOnly,
        ListingCreatingPermission,
        ListingModifyingPermission,
    )

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user)
