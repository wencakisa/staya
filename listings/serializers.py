from rest_framework import serializers

from users.serializers import UserDetailsSerializer
from .models import Location, Amenity, Listing


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'longitude', 'latitude')


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name')


class ListingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=256)
    resident = UserDetailsSerializer(read_only=True)
    amenities = AmenitySerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = Listing
        fields = ('id', 'title', 'description', 'resident', 'amenities', 'location')

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        amenities_data = validated_data.pop('amenities')

        location, _ = Location.objects.get_or_create(**location_data)
        listing = Listing.objects.create(location=location, **validated_data)

        for amenity_data in amenities_data:
            listing.amenities.add(Amenity.objects.get(**amenity_data))

        return listing
