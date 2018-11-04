from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    message = 'You can view only your own bookings.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsResidentUser(permissions.BasePermission):
    message = 'You have to be a resident user in order to access this view.'

    def has_permission(self, request, view):
        return request.user.is_resident


class ListingCreatingPermission(IsResidentUser):
    message = 'You have to be a resident user in order to create listings.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class ListingModifyingPermission(permissions.BasePermission):
    message = 'You can only modify your own listings.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.resident == request.user


class BaseNestedListingResourcePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.resident != request.user


class ListingBookingPermission(BaseNestedListingResourcePermission):
    message = 'You can not book your own listings.'


class ListingReviewPermission(BaseNestedListingResourcePermission):
    message = 'You can not review your own listings.'


class ListingIsUnbookedYet(permissions.BasePermission):
    pass
