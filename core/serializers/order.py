import json
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Order, OrderPoint, OrderTechnics, TechnicsSubType, OrderRequestToDispatcher
from ..serializers.technics import AutoSerializer


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPoint
        fields = ('id', 'order', 'latitude', 'longitude', 'description')


class TechnicsSerializer(serializers.ModelSerializer):
    autos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    subtypes = serializers.PrimaryKeyRelatedField(many=True, queryset=TechnicsSubType.objects.all(), required=False)

    class Meta:
        model = OrderTechnics
        fields = ('id', 'order', 'tech_type', 'quantity', 'autos', 'subtypes')

    def validate(self, data):
        if not (data.get('tech_type', None) or data.get('subtypes', None)):
            raise serializers.ValidationError("'tech_type' or 'subtypes' is required.")
        return super().validate(data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTechnics
        fields = ('id', 'order', 'image', 'description')


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'started_at', 'ended_at', 'description', 'is_closed')

    def create(self, validated_data):
        return Order.objects.create(client=self.context['request'].user, **validated_data)


class OrderDetailSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    technics = TechnicsSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'started_at', 'ended_at', 'description', 'is_closed', 'points', 'technics', 'images')


class FilterSerializer(serializers.Serializer):
    pass


class OrderRequestToDispatcherSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer()
    autos = AutoSerializer(many=True)

    class Meta:
        model = OrderRequestToDispatcher
        fields = ('id', 'order', 'autos')
