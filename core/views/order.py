import random
import requests
from hashlib import sha1
from datetime import datetime, timedelta
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from gt.settings import WEBPAY
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.permissions import IsAuthenticatedDispatcher, IsAuthenticatedClient
from ..permissions import IsOrderOwner
from geopy.distance import geodesic

from ..models import Order, OrderPoint, OrderTechnics, OrderImage, Auto, TechnicsType, OrderRequestToDispatcher
from user.models import Driver
from ..serializers.order import CreateOrderSerializer, OrderDetailSerializer, PointSerializer, \
    TechnicsSerializer, ImageSerializer

import logging
logger = logging.getLogger(__name__)


class OrderListPagination(PageNumberPagination):
    page_size = 50


class OrderList(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    GET: Get all orders by client.
    POST: Add Order by client.
    Authorization required.
    """
    serializer_class = CreateOrderSerializer
    permission_classes = (IsAuthenticatedClient,)
    pagination_class = OrderListPagination

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


class SearchOrderList(viewsets.GenericViewSet):
    """
    POST: Get Orders using filter or/and sort.
    Authorization required.
    """
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = OrderListPagination

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'dispatcher'):
            return Order.objects.filter(dispatcher=user)
        if hasattr(user, 'clientprivate') or hasattr(user, 'clientlegal'):
            return Order.objects.filter(client=user)

    def search(self, request, *args, **kwargs):
        """
        {
            "filter": {
                "is_confirm": False,
                "is_complete": False,
                "is_paid": False,
                "is_closed": False,
            },
            "sort": ["-created_at", "price"...]
        }
        """
        queryset = self.get_queryset()
        filter_data = request.data.pop('filter', None)
        sort_data = request.data.pop('sort', None)

        if filter_data is not None:
            # ! Write serializer for filter to validate data !
            attrs = filter(lambda i: hasattr(Order(), i), filter_data.keys())
            filter_data = dict((k, v) for k, v in filter_data.items() if k in attrs)
            queryset = queryset.filter(**filter_data)

        if sort_data is not None:
            attrs = set([i[1:] if i[:1] == '-' else i for i in sort_data])
            attrs = [i for i in attrs if hasattr(Order(), i)]
            sort_data = [i for i, _ in zip(sort_data, attrs) if i[1:] in attrs or i in attrs]
            queryset = queryset.order_by(*sort_data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Get, update, delete Order.
    Allowed HTTP methods: GET, PUT, PATCH, DELETE
    Authorization required.
    """
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticatedClient, )

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CreateListOrOneModelMixin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Allow create as a list of objects as a one object.
    inherited from mixins.CreateModelMixin and viewsets.GenericViewSet
    """
    def create(self, request, *args, **kwargs):
        # add possibility create many objects
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def check_order(order_id, user):
    order = get_object_or_404(Order.objects.select_related().prefetch_related(), pk=order_id)
    if not order.client == user:
        raise AuthenticationFailed('This order does not belong to this user.')
    return order


class CreatePointView(CreateListOrOneModelMixin):
    """
    POST: Add Point or many Points by client.
    Authorization required.
    """
    queryset = OrderPoint.objects.all()
    serializer_class = PointSerializer
    permission_classes = (IsAuthenticatedClient,)

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs[self.lookup_field]
        order = check_order(order_id, request.user)
        count = order.points.count()
        if count >= 7:
            return Response('Order {} already has 7 points.')
        if isinstance(request.data, list):
            if len(request.data) + count >= 7:
                return Response('Order {} already has {} points. You want add another {} points.'
                                .format(order_id, count, len(request.data)))
            for point in request.data:
                point.update(order=order_id)
        else:
            request.data.update(order=order_id)

        return self.create(request, *args, **kwargs)


class CreateTechicsView(CreateListOrOneModelMixin):
    """
    POST: Add Technic or many Technics by client.
    Authorization required.
    """
    queryset = OrderTechnics.objects.all()
    serializer_class = TechnicsSerializer
    permission_classes = (IsAuthenticatedClient,)

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs[self.lookup_field]
        order = check_order(order_id, request.user)
        if isinstance(request.data, list):
            for technic in request.data:
                technic.update(order=order_id)
        else:
            request.data.update(order=order_id)

        return self.create(request, *args, **kwargs)


class CreateImagesView(CreateListOrOneModelMixin):
    """
    POST: Add Image or many Images by client.
    Authorization required.
    """
    queryset = OrderImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedClient,)
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs[self.lookup_field]
        check_order(order_id, request.user)
        if isinstance(request.data, list):
            for image in request.data:
                image.update(order=order_id)
        else:
            request.data.update(order=order_id)

        return self.create(request, *args, **kwargs)


def find_mobile(point, auto_ids, radius=200):
    """
    Search autos in a given radius using cache.
    Return a dictionary:
        { auto_id: (parking_latitude, parking_longitude), ... }
    """
    autos = cache.get('autos_parking_places')

    if autos is None:
        autos = dict(
            (auto.id, (auto.parking_latitude, auto.parking_longitude))
            for auto in Auto.objects.exclude(is_active=False).only('id', 'parking_latitude', 'parking_longitude')
        )
        cache.set('autos_parking_places', autos, 60)
    ids = [pk for pk, location in autos.items()
                if pk in auto_ids and geodesic(point, location).kilometers <= radius]
    # logger.debug("Auto ids: {}".format(auto_ids))
    return set(ids)


def get_calendar():
    calendar = cache.get('calendar')
    if calendar is not None:
        return calendar

    orders_qset = Order.objects.exclude(is_closed=True, ended_at__gt=datetime.now() + timedelta(hours=1))\
        .prefetch_related('technics__autos__auto')
    calendar = dict()
    for order in orders_qset.all():
        for technic in order.technics.all():
            for unit_tech in technic.autos.all():
                a = calendar.get(unit_tech.auto.id, None)
                if a is not None:
                    a.append((order.started_at, order.ended_at))
                else:
                    calendar.update({unit_tech.auto.id: [(order.started_at, order.ended_at)]})
    cache.set('calendar', calendar, 60)

    return calendar


class ConfirmOrderView(APIView):
    permission_classes = (IsAuthenticatedClient,)

    def post(self, request, pk, format='json'):
        # check order and set as confirmed
        order = check_order(pk, request.user)
        if not order.points.exists():
            return Response('Order {} has no any points.'.format(pk), status=status.HTTP_400_BAD_REQUEST)
        if not order.technics.exists():
            return Response('Order {} has no any technics.'.format(pk), status=status.HTTP_400_BAD_REQUEST)
        order.is_confirm = True
        order.save()

        # filter autos by technic types
        auto_qset = Auto.objects.select_related('subtype')
        res_auto_qset = Auto.objects.none()
        for technic in order.technics.all():
            subtypes = technic.subtypes.all()
            tech_type = technic.tech_type
            if subtypes:
                qset = auto_qset.filter(subtype__in=subtypes)
            else:
                qset = auto_qset.filter(subtype__in=tech_type.subtypes.all())
            res_auto_qset = res_auto_qset.union(qset)

        # filter autos by weather

        # filter autos by technics that are not busy
        busy_autos_ids = []
        for id, value in get_calendar().items():
            for time_from, time_to in value:
                if not (
                            (order.started_at < time_from and order.ended_at < time_from)
                        or
                            (order.started_at > time_to and order.ended_at > time_to)
                ):
                    busy_autos_ids.append(id)

        auto_ids = set(item['id'] for item in res_auto_qset.values('id'))
        auto_ids -= set(busy_autos_ids)

        # find autos in the distances
        point = order.points.first()
        res_autos_ids = []
        for distance in [15, 25, 50, 100, 200]:
            if not auto_ids:
                break
            ids = find_mobile((point.latitude, point.longitude), auto_ids, distance)
            res_autos_ids.append(ids)
            auto_ids -= ids

        if not [s for s in res_autos_ids if s]:
            return Response("There are not any technics.", status=status.HTTP_204_NO_CONTENT)

        # request to dispatchers
        dispatchers_ids = set(item['dispatcher'] for item in res_auto_qset.values('dispatcher').distinct('dispatcher'))

        now = datetime.now()
        delta_time = 0
        for dispatcher in dispatchers_ids:
            for ids in res_autos_ids:
                if res_auto_qset.filter(pk__in=ids).exists():
                    autos = res_auto_qset.filter(pk__in=ids, dispatcher=dispatcher).all()
                    # OrderRequestToDispatcher.objects.bulk_create([
                    #     OrderRequestToDispatcher(
                    #         order=order, autos=autos, time_from=(now + timedelta(minutes=delta_time))
                    #     )
                    # ])
                    delta_time += 1

        return Response()


class PaymentsNotificationView(APIView):
    def post(self,request):
        order = get_object_or_404(Order, pk=request.data['site_order_id'])
        if request.data['payment_type'] == 1 or request.data['payment_type'] == 4:
            order.transaction_id = request.data['transaction_id']
            order.save()
        return Response()

class PaymentsReturnsView(APIView):
    def get(self,request, status):
        params = request.query_params
        order = Order.objects.get(params['wsb_order_num'])
        if status == 'success':
            order.transaction_id = params['wsb_tid']
            order.save()

        if status == 'cancel':

            Response(data={'status': "Заказ № {} не оплачен".format(order.id)})



class OrderPaymentView(APIView):
    def get(self,request, pk, pk1):
        order = get_object_or_404(Order, pk=pk)
        WEBPAY['total'] = random.randint(100,500)
        WEBPAY['seed'] = str(datetime.utcfromtimestamp(datetime.now().second))
        WEBPAY['signature'] = sha1((WEBPAY['seed'] + WEBPAY['wsb_storeid'] + str(order.id) + str(WEBPAY["test"]) +
                                    WEBPAY['wsb_currency_id'] + str(WEBPAY['total']) + WEBPAY["secret_key"])
                                   .encode('utf-8')).hexdigest()
        form_data = {
            '*scart': "",
            'wsb_version': "2",
            'wsb_storeid': WEBPAY['wsb_storeid'],
            'wsb_store': WEBPAY['wsb_store'],
            'wsb_test': WEBPAY['test'],
            'wsb_currency_id': WEBPAY['wsb_currency_id'],
            'wsb_seed': WEBPAY['seed'],
            'wsb_signature': WEBPAY['signature'],
            'wsb_order_num': str(order.id),
            'wsb_invoice_item_name[0]': str(order),
            'wsb_invoice_item_quantity[0]': "1",
            'wsb_invoice_item_price[0]' : str(order.total),
            'wsb_total': str(order.total),

        }
        if pk1 == 'erip':
            url = 'https://payment.webpay.by/'
            form_data['wsb_storeid'] = WEBPAY['wsb_storeid_erip']
            WEBPAY['signature'] = sha1((WEBPAY['seed'] + WEBPAY['wsb_storeid'] + str(order.id) + str(WEBPAY["test"]) +
                                        WEBPAY['wsb_currency_id'] + str(WEBPAY['total']) + WEBPAY["secret_key"])
                                       .encode('utf-8')).hexdigest()
            form_data['wsb_signature'] = WEBPAY['signature']
            r = requests.request("POST", url=url, data=form_data)
            return Response(data={'order': order.id})


        return Response(data={'order': order.id, 'form': form_data})
