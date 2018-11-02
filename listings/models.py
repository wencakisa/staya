from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Location(models.Model):
    name = models.CharField(max_length=256)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return f'{self.name} [{self.longitude}; {self.latitude}]'


class Amenity(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'amenities'

    def __str__(self):
        return self.name


class Listing(models.Model):
    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'is_resident': True}
    )
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=10000, blank=True)
    price_per_night = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='listings')

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.__class__.__name__} #{self.id} for {self.listing}'


class Review(models.Model):
    REVIEW_MIN_SCORE = 0
    REVIEW_MAX_SCORE = 5
    REVIEW_SCORE_VALIDATORS = [
        MinValueValidator(REVIEW_MIN_SCORE),
        MaxValueValidator(REVIEW_MAX_SCORE)
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(default=0, validators=REVIEW_SCORE_VALIDATORS)
    text = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.__class__.__name__} for {self.listing} by {self.user} ({self.score})'
