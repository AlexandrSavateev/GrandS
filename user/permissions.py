from rest_framework.permissions import BasePermission
from core.models.order import Order

class IsAuthenticatedDispatcher(BasePermission):
    """
        Allows access only to authenticated dispatchers.
    """

    def has_permission(self, request, view):
        is_dispatcher = hasattr(request.user, 'dispatcher')
        return request.user and request.user.is_authenticated and is_dispatcher


class IsAuthenticatedClient(BasePermission):
    """
        Allows access only to authenticated client.
    """

    def has_permission(self, request, view):
        user = request.user
        is_client = hasattr(user, 'clientprivate') or hasattr(user, 'clientlegal')
        return user and user.is_authenticated and is_client
