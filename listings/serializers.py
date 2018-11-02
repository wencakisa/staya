from rest_framework import serializers

from users.serializers import UserDetailsSerializer
from .models import Location, Amenity, Listing, Booking, Review


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'longitude', 'latitude')


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'check_in', 'check_out')

    def validate(self, data):
        if data['check_in'] > data['check_out']:
            raise serializers.ValidationError('Check in should be before check out.')

        return data


class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'score', 'text')


class ListingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=256)
    resident = UserDetailsSerializer(read_only=True)
    amenities = AmenitySerializer(many=True)
    location = LocationSerializer()
    bookings = BookingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = (
            'id',
            'title', 'description', 'price_per_night',
            'resident', 'location',
            'amenities', 'bookings', 'reviews',
        )

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        amenities_data = validated_data.pop('amenities')

        location, _ = Location.objects.get_or_create(**location_data)
        listing = Listing.objects.create(location=location, **validated_data)

        for amenity_data in amenities_data:
            listing.amenities.add(Amenity.objects.get(**amenity_data))

        return listing
