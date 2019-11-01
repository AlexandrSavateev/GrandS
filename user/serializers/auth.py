from django.conf import settings
from rest_framework import serializers, exceptions
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                               get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from django.contrib.auth import get_user_model, authenticate
UserModel = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_phone(self, phone):
        phone = get_adapter().clean_username(phone)
        return phone

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "Пользователь с таким e-mail уже существует.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Введенные пароли не совпадают.")
        return data

    def get_cleaned_data(self):
        return {
            'phone': self.validated_data.get('phone', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = UserModel.objects.create_user(
            phone=self.cleaned_data.get('phone'),
            password=self.cleaned_data.get('password1'),
            email=self.cleaned_data.get('email')
        )
        user.save()
        setup_user_email(request, user, [])
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_phone(self, phone, password):
        user = None

        if phone and password:
            user = authenticate(username=phone, password=password)
        else:
            msg = 'Должны быть включены поля "phone" и "password".'
            raise exceptions.ValidationError(msg)

        return user

    def _validate_phone_email(self, phone, email, password):
        user = None

        if phone and password:
            user = authenticate(username=phone, password=password)
        elif email and password:
            try:
                user_obj = UserModel.objects.get(email=email)
                user = authenticate(username=user_obj.phone, password=password)
            except UserModel.DoesNotExist:
                msg = 'Не найден пользователь с таким email: {}'.format(email)
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Должны быть включены поля "phone" или "email" и "password".'
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        phone = attrs.get('phone')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        # Authentication through username
        if allauth_settings.AUTHENTICATION_METHOD == allauth_settings.AuthenticationMethod.USERNAME:
            user = self._validate_phone(phone, password)

        # Authentication through either username or email
        else:
            user = self._validate_phone_email(phone, email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'Аккаунт не активен.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Не возможно войти с предоставленными данными.'
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError('E-mail не подтвержден.')

        attrs['user'] = user
        return attrs


class UserAuthResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'phone', 'email', 'user_type')
        read_only = True
