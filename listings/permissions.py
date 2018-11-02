from rest_framework import permissions


class ListingCreatingPermission(permissions.BasePermission):
    message = 'You have to be a resident user in order to create listings.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_resident


class ListingModifyingPermission(permissions.BasePermission):
    message = 'You can only modify your own listings.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.resident == request.user


class ListingBookingPermission(permissions.BasePermission):
    message = 'You can not book your own listings.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.resident != request.user
