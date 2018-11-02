from django.contrib import admin

from listings.admin import ListingInline
from .models import User


class UserAdmin(admin.ModelAdmin):
    inlines = [ListingInline,]

admin.site.register(User, UserAdmin)
