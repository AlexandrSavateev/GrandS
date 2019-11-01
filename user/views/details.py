from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.serializers.details import ClientPrivateDetailsSerializer, ClientLegalDetailsSerializer, \
    DispatcherDetailsSerializer, DriverSerializer
from ..permissions import IsAuthenticatedDispatcher
from user.models import Driver
from django.contrib.auth import get_user_model
import logging

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class ClientPrivateDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientPrivateDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user.clientprivate
        return user


class ClientLegalDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientLegalDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user.clientlegal
        return user


class DispatcherDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = DispatcherDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user.dispatcher
        return user


class DriverByDispatcherList(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    GET: List of drivers owned by the dispatcher.
    POST: Add driver with owner is the dispatcher.
    Authorization required.
    """
    serializer_class = DriverSerializer
    permission_classes = (IsAuthenticatedDispatcher,)

    def get_queryset(self):
        return Driver.objects.filter(dispatcher=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DriverByDispatcherDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Get, create, update Auto.
    Allowed HTTP methods: GET, PUT, PATCH, DELETE
    Authorization required.
    """
    serializer_class = DriverSerializer
    permission_classes = (IsAuthenticatedDispatcher,)

    def get_queryset(self):
        return Driver.objects.filter(dispatcher=self.request.user)

    def get_object(self):
        # overwrite because there is used id of binding user objects
        queryset = self.filter_queryset(self.get_queryset())
        obj = generics.get_object_or_404(queryset, user_id=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
