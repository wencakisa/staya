from django.contrib import admin

from .models import Amenity, Listing


class ListingInline(admin.StackedInline):
    model = Listing


admin.site.register(Amenity)
admin.site.register(Listing)
