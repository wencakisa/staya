from rest_framework import viewsets

from .models import Listing
from .serializers import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

    # TODO: Implement permissions and add permission_classes

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user)
