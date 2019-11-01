"""
Django settings for gt project.
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=t#xz966bvhp=3d@v9!lr6-lq3qyreraib-c!fc9=e=_-2w&li'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    'user',
    'rest_framework',
    'rest_framework_recursive',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',

    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'bootstrap4',
    'corsheaders',

    'core'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'gt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'gt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gt_database',
        'USER': 'gt_user',
        'PASSWORD': 'gt_user',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True
# DATE_FORMAT = "%d.%m.%Y"
# DATE_INPUT_FORMATS = ["%d.%m.%Y"]
# DATETIME_INPUT_FORMATS = ["%d.%m.%Y %H:%M:%S"]

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'gt/static'))
STATICFILES_DIRS = [
    os.path.abspath(os.path.join(BASE_DIR, 'gt/assets'))
]

MEDIA_URL = '/media/'
PATH_TO_SAVE_XML = os.path.abspath(os.path.join(BASE_DIR, 'gt/xml'))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'gt/media'))


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# as backend for authentication we use custom model: User ? (Egor Chernik)
AUTH_USER_MODEL = 'user.User'

# Django-rest-auth
SITE_ID = 1
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.auth.UserAuthResponseSerializer',
    'LOGIN_SERIALIZER': 'user.serializers.auth.UserLoginSerializer'
}

# Django-rest-framework-jwt
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(hours=8),   # default: seconds=300
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# Django-allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_EMAIL_REQUIRED = False    # = ACCOUNT_EMAIL_REQUIRED
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5    # default 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300   # default 300 sec
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'
ACCOUNT_USERNAME_VALIDATORS = 'user.validators.phone_validators'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'


PRICE_DAYOFF_RATE = 1.1

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gt.bps.by@gmail.com'
EMAIL_HOST_PASSWORD = 'kBgrjdcrFz'
EMAIL_PORT = 587

# bePaid
# BASE_DOMAIN = 'http://gt.by/payment/'

# BEPAID = {
#     'TEST': True,
#     'SHOP_ID': '4772',
#     'KEY': 'ccd00a86a3c1680085d1bb539a7614bdfecd9f7d39aac66f6626457b3c4afa0c',
#     'SUCCESS_URL': BASE_DOMAIN + 'success/',
#     'DECLINE_URL': BASE_DOMAIN + 'decline/',
#     'FAIL_URL': BASE_DOMAIN + 'fail/',
#     'NOTIFICATION_URL': BASE_DOMAIN + 'notification',
#     'ERIP_NOTIFICATION_URL': BASE_DOMAIN + 'erip_notification',
#     'ERIP_SERVICE_NO': '',
#     # описание пути в дереве ЕРИП для нахождения платежного поручения
#     'ERIP_INSTRUCTION': [' ']
# }

# WebPay
BASE_DOMAIN = 'http://test.blackzerg.pro/'
WEBPAY = {
    "test": '1',  # 0 - FALSE/1 - TRUE
    "wsb_storeid": '181018160',
    "wsb_storeid_erip": '181018160',
    "wsb_store": 'GT.BY',
    "wsb_version": '2',
    "wsb_currency_id": "BYN",
    "secret_key": 'VXt%-7Smt2jMh$-6',
    "notification_url": BASE_DOMAIN + 'orders/payments/notification/',
    "return_url": BASE_DOMAIN + 'orders/payments/success/',
    "cancel_return_url": BASE_DOMAIN + 'orders/payments/cancel/',
}

# Yandex Forecast
YANDEX_API_KEY = ''
