from django.contrib import admin

from .models import Location, Amenity, Listing, ListingImage, Booking, Review


class ListingInline(admin.StackedInline):
    model = Listing


admin.site.register(Location)
admin.site.register(Amenity)
admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(ListingImage)
