from django.contrib import admin

from .models import Location, Amenity, Listing


class ListingInline(admin.StackedInline):
    model = Listing


admin.site.register(Location)
admin.site.register(Amenity)
admin.site.register(Listing)
