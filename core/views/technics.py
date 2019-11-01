from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.permissions import IsAuthenticatedDispatcher

from ..models import TechnicsCategory, Auto
from user.models import Driver
from ..serializers.technics import CategorySerializer, AutoSerializer


# def get_driver_by_id(id):
#     try:
#         return Driver.objects.get(pk=id)
#     except Driver.DoesNotExist:
#         raise NotFound(detail={'errors': ['Не найден водитель с таким id: {}'.format(id)]}, code=404)
#
#
# def get_mobile_by_id(id):
#     try:
#         return Avtomobile.objects.get(pk=id)
#     except Avtomobile.DoesNotExist:
#         raise NotFound(detail={'errors': ['Не найдена техника с таким id: {}'.format(id)]}, code=404)
#
#
# def get_category_by_id(id):
#     try:
#         return TechCategory.objects.get(pk=id)
#     except TechCategory.DoesNotExist:
#         raise NotFound(detail={'errors': ['Не найдена категория с таким id: {}'.format(id)]}, code=404)


class CategoryView(generics.ListAPIView):
    queryset = TechnicsCategory.objects.all()
    serializer_class = CategorySerializer


class AutoByDispatcherList(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    GET: List of autos owned by the dispatcher.
    POST: Add auto with owner is the dispatcher.
    Authorization required.
    """
    serializer_class = AutoSerializer
    permission_classes = (IsAuthenticatedDispatcher,)

    def get_queryset(self):
        return Auto.objects.filter(dispatcher=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AutoByDispatcherDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Get, update, delete Auto.
    Allowed HTTP methods: GET, PUT, PATCH, DELETE
    Authorization required.
    """
    serializer_class = AutoSerializer
    permission_classes = (IsAuthenticatedDispatcher,)

    def get_queryset(self):
        return Auto.objects.filter(dispatcher=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
