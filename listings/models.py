from django.db import models

from users.models import User


class Amenity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Listing(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=10000, blank=True, null=True)
    amenities = models.ManyToManyField(Amenity)

    def __str__(self):
        return self.title
