from rest_framework import serializers, exceptions
from user.models import (ClientLegal, ClientPrivate,
                         Dispatcher, Driver, Address, Organization)
from allauth.account.adapter import get_adapter
from core.models.technics import Auto
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'street', 'house', 'housing', 'office', 'description')


class OrganizationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    post_address = AddressSerializer(required=False)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'unp', 'address', 'post_address', 'bank', 'bank_department',
                  'bank_address', 'bank_bik', 'contact_org', 'iban', 'first_person', 'acting_on',
                  'accountant', 'contact_person', 'add_contact', 'certificate')

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        post_address_data = validated_data.pop('post_address', None)
        address = Address.objects.create(**address_data)
        post_address = Address.objects.create(**post_address_data)
        org = Organization.objects.create(address=address, post_address=post_address, **validated_data)

        return org

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        post_address_data = validated_data.pop('post_address', None)
        address = instance.address
        post_address = instance.post_address
        if address_data:
            address_ser = AddressSerializer(address, address_data)
            if address_ser.is_valid(raise_exception=True):
                address_ser.save()
        if post_address_data:
            post_address_ser = AddressSerializer(post_address, post_address_data)
            if post_address_ser.is_valid(raise_exception=True):
                post_address_ser.save()

        super().update(instance, validated_data)

        return instance


class ClientPrivateDetailsSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = ClientPrivate
        fields = ('id', 'phone', 'email', 'first_name', 'last_name', 'patronymic',
                  'birth_date', 'person_id', 'address', 'image')

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        client = ClientPrivate.objects.create(**validated_data)
        Address.objects.create(client=client, **address_data)
        return client

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        address = instance.address
        if address_data:
            address_ser = AddressSerializer(address, address_data)
            if address_ser.is_valid(raise_exception=True):
                address_ser.save()

        super().update(instance, validated_data)

        return instance


class ClientLegalDetailsSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False)

    class Meta:
        model = ClientLegal
        fields = ('id', 'phone', 'email', 'organization', 'image', 'first_name', 'last_name', 'patronymic')

    def create(self, validated_data):
        organization_data = validated_data.pop('organization', None)
        organization_ser = OrganizationSerializer(data=organization_data)
        if organization_ser.is_valid(raise_exception=True):
            organization = organization_ser.save()
        client = ClientPrivate.objects.create(organization=organization, **validated_data)

        return client

    def update(self, instance, validated_data):
        organization_data = validated_data.pop('organization', None)
        organization = instance.organization
        if organization_data:
            org_ser = OrganizationSerializer(organization, organization_data)
            if org_ser.is_valid(raise_exception=True):
                org_ser.save()

        super().update(instance, validated_data)

        return instance


class DispatcherDetailsSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False)

    class Meta:
        model = ClientLegal
        fields = ('id', 'phone', 'email', 'organization', 'image', 'first_name', 'last_name', 'patronymic')

    def create(self, validated_data):
        organization_data = validated_data.pop('organization', None)
        organization_ser = OrganizationSerializer(data=organization_data)
        if organization_ser.is_valid(raise_exception=True):
            organization = organization_ser.save()
        dispatcher = ClientPrivate.objects.create(organization=organization, **validated_data)

        return dispatcher

    def update(self, instance, validated_data):
        organization_data = validated_data.pop('organization', None)
        organization = instance.organization
        if organization_data:
            org_ser = OrganizationSerializer(organization, organization_data)
            if org_ser.is_valid(raise_exception=True):
                org_ser.save()

        super().update(instance, validated_data)

        return instance


class AutoSerializerForDriver(serializers.ModelSerializer):

    title = serializers.CharField(source='subtype.tech_type.title', required=False)
    class Meta:
        model = Auto
        fields = ('id', 'model', 'number', 'title')


class DriverSerializer(serializers.Serializer):
    # there is used id of binding user objects
    id = serializers.IntegerField(source='user.id', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', required=False)
    phone = serializers.CharField(source='user.phone')
    email = serializers.EmailField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    patronymic = serializers.CharField(source='user.patronymic', required=False)
    birth_date = serializers.DateField(source='user.birth_date', required=False)
    image = serializers.ImageField(source='user.image', required=False)

    status = serializers.ModelField(model_field=Driver()._meta.get_field('status'), required=False)
    autos = AutoSerializerForDriver(many=True, read_only=True, allow_null=True)

    def validate_phone(self, phone):
        phone = get_adapter().clean_username(phone)
        return phone

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data.pop('user', None))
        user.save()
        driver = Driver.objects.create(
            dispatcher=self.context['request'].user.dispatcher,
            user=user,
            **validated_data)
        return driver

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        user = instance.user

        user.is_active = user_data.get('is_active', user.is_active)
        user.phone = user_data.get('phone', user.phone)
        user.email = user_data.get('is_active', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.patronymic = user_data.get('patronymic', user.patronymic)
        user.birth_date = user_data.get('birth_date', user.birth_date)
        user.image = user_data.get('image', user.image)
        user.save()

        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance
