from math import cos
from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


def listing_image_directory_path(instance, filename):
    return f'listings/{instance.listing.id}/{filename}'


class Location(models.Model):
    LAT_DEGREE_TO_KM = 110.574
    LONG_DEGREE_TO_KM = 111.320 * cos(LAT_DEGREE_TO_KM)
    NEARBY_KM_LAT = LAT_DEGREE_TO_KM * 0.005
    NEARBY_KM_LONG = LONG_DEGREE_TO_KM * 0.005

    title = models.CharField(max_length=256)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return f'{self.title} [{self.longitude}; {self.latitude}]'


class Amenity(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'amenities'

    def __str__(self):
        return self.name


class Listing(models.Model):
    LISTING_MIN_GUEST_AMOUNT = 0
    LISTING_MAX_GUEST_AMOUNT = 21
    LISTING_GUEST_AMOUNT_VALIDATORS = [
        MinValueValidator(LISTING_MIN_GUEST_AMOUNT),
        MaxValueValidator(LISTING_MAX_GUEST_AMOUNT)
    ]

    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'is_resident': True}
    )
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=10000, blank=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    guest_amount = models.PositiveSmallIntegerField(validators=LISTING_GUEST_AMOUNT_VALIDATORS)
    amenities = models.ManyToManyField(Amenity)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='listings')

    def __str__(self):
        return self.title

    @property
    def reviews_score_sum(self):
        return self.reviews.aggregate(sum=models.Sum('score'))['sum']

    @property
    def total_reviews(self):
        return self.reviews.count()

    @property
    def average_review_score(self):
        if self.reviews_score_sum is None:
            return 0

        return self.reviews_score_sum / self.total_reviews


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=listing_image_directory_path)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()

    class Meta:
        ordering = ['-check_in']

    def __str__(self):
        return f'{self.__class__.__name__} #{self.id} for {self.listing}'

    @classmethod
    def current_bookings(cls):
        return cls.objects.filter(check_out__lte=date.today())


class Review(models.Model):
    REVIEW_MIN_SCORE = 0
    REVIEW_MAX_SCORE = 5
    REVIEW_SCORE_VALIDATORS = [
        MinValueValidator(REVIEW_MIN_SCORE),
        MaxValueValidator(REVIEW_MAX_SCORE)
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(validators=REVIEW_SCORE_VALIDATORS)
    text = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.__class__.__name__} for {self.listing} by {self.user} ({self.score})'
