from django.db import models

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
