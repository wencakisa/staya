from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

import cloudinary

from users.serializers import UserDetailsSerializer
from .models import Location, Amenity, Listing, ListingImage, Booking, Review


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'title', 'longitude', 'latitude')


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


class ListingImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = ListingImage
        fields = ('id', 'image', 'image_url')


class ListingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=256)
    resident = UserDetailsSerializer(read_only=True)
    location = LocationSerializer()
    amenities = AmenitySerializer(many=True)
    bookings = BookingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ListingImageSerializer(many=True)

    class Meta:
        model = Listing
        fields = (
            'id',
            'title', 'description', 'price_per_night', 'guest_amount',
            'total_reviews', 'average_review_score',
            'resident', 'location', 'location',
            'amenities', 'bookings', 'reviews', 'images',
        )

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        amenities_data = validated_data.pop('amenities')
        images_data = validated_data.pop('images')

        location, _ = Location.objects.get_or_create(**location_data)
        listing = Listing.objects.create(location=location, **validated_data)

        for amenity_data in amenities_data:
            listing.amenities.add(Amenity.objects.get(**amenity_data))

        for image_data in images_data:
            image = image_data['image']
            upload_hash = cloudinary.uploader.upload(image, use_filename=True)
            image_url = upload_hash['secure_url']

            ListingImage.objects.create(listing=listing, image=image, image_url=image_url)

        return listing


class UserBookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'check_in', 'check_out', 'listing')
