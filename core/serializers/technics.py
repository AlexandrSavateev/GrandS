from rest_framework import serializers
# from rest_framework_recursive.fields import RecursiveField
from ..models import TechnicsCategory, TechnicsType, TechnicsSubType, Auto
from django.contrib.auth import get_user_model
from collections import OrderedDict

UserModel = get_user_model()


class SubTypeSerializer(serializers.ModelSerializer):
    autos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = TechnicsSubType
        fields = ('__all__')

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        return OrderedDict((k, v) for k, v in ret.items() if v)


class TypeSerializer(serializers.ModelSerializer):
    subtypes = SubTypeSerializer(many=True)

    class Meta:
        model = TechnicsType
        fields = ('id', 'title', 'subtypes')


class CategorySerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True)

    class Meta:
        model = TechnicsCategory
        fields = ('id', 'title', 'types')


class AutoSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='subtype.tech_type.category', required=False)
    first_name_driver = serializers.CharField(source='driver.user.first_name', required=False)
    last_name_driver = serializers.CharField(source='driver.user.last_name', required=False)
    patronymic_driver = serializers.CharField(source='driver.user.patronymic', required=False)
    phone_driver = serializers.CharField(source='driver.user.phone', required=False)
    class Meta:
        model = Auto
        fields = ('id', 'category', 'first_name_driver','patronymic_driver','phone_driver','last_name_driver', 'model',
                  'brand','number', 'year', 'image', 'description',
                  'parking_latitude', 'parking_longitude', 'parking_description',
                  'road_restriction', 'relocation', 'is_active')

    def create(self, validated_data):
        return Auto.objects.create(dispatcher=self.context['request'].user.dispatcher, **validated_data)
