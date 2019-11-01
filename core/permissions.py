from rest_framework.permissions import BasePermission
from core.models.order import Order


class IsOrderOwner(BasePermission):
    """
        Allows access only to owner of order.
    """
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
