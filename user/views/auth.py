import json
import string
import requests
from random import choice, randint

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_auth.registration.views import RegisterView
from user.smsc_api import *
from django.core.mail import send_mail
from gt.settings import PATH_TO_SAVE_XML
import xml.etree.ElementTree as ET

from user.serializers.auth import UserRegistrationSerializer
from user.serializers.details import *
from user.models import ClientPrivate, ClientLegal, Dispatcher

from django.contrib.auth import get_user_model
import logging

UserModel = get_user_model()
logger = logging.getLogger(__name__)


def get_rand_int(min_char, max_char):
    allchar = string.digits
    return "".join(choice(allchar) for x in range(randint(min_char, max_char)))


def send_sms(phone):
    """
    Отправка СМС.
    Убрать заглушку и раскоментировать отправку СМС
    """
    smsc = SMSC()
    code = get_rand_int(4, 5)

    print("SMS на номер: {} Ваш пароль: {}".format(phone, code))

    # result = smsc.send_sms(
    #     phone, " Ваш пароль: {}".format(code), sender="sms"
    # )
    return code


def send_call(phone):
    """
    Совершение звонка.
    """
    url = 'https://smsc.ru/sys/send.php'
    data = {
        "login": SMSC_LOGIN,
        "psw": SMSC_PASSWORD,
        "phones": phone,
        "mes": "code",
        "call": 1,
        "fmt": 3
    }
    r = requests.get(url, params=data)
    resp = json.loads(r.text)
    return resp.get("code")


def get_user_by_phone(phone):
    try:
        return UserModel.objects.get(phone=phone)
    except UserModel.DoesNotExist:
        raise NotFound(
            detail={'errors': ['Не найден пользователь с таким телефоном: {}'.format(phone)]},
            code=404
        )


def get_user_by_email(email):
    try:
        return UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        raise NotFound(
            detail={'errors': ['Не найден пользователь с таким email: {}'.format(email)]},
            code=404
        )


# def write_xml(data):
#     name = datetime.now()
#     mydata = ET.tostring(data)
#     mydata = mydata.decode("utf-8")
#     with open(os.path.abspath(os.path.join(PATH_TO_SAVE_XML, "{}.xml".format(name))), "w") as out:
#         out.write(mydata)
#
#
# def send_xml(user):
#     data = ET.Element("client-data")
#     udict = user.get_userfield()
#     for param in udict:
#         item = ET.SubElement(data, param)
#         item.text = udict.get(param)
#     write_xml(data)


class BaseSigUpView(RegisterView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        is_call = request.data.get('is_call')
        phone = request.data.get('phone')
        if is_call is not None:
            code = send_call(phone)
        else:
            code = send_sms(phone)
        resp.data.update(sms_code=code)
        logger.debug('{}'.format(resp.data))
        return resp


class ClientPrivateSigUpView(BaseSigUpView):

    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        # create ClientPrivate object in database
        client = ClientPrivate()
        client.user_ptr = user
        client.user_ptr.user_type = 1
        client.user_ptr.save_base()
        client.save_base(raw=True)
        return user


class ClientLegalSigUpView(BaseSigUpView):

    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        # create ClientLegal object in database
        client = ClientLegal()
        client.user_ptr = user
        client.user_ptr.user_type = 2
        client.user_ptr.save_base()
        client.save_base(raw=True)
        return user


class DispatcherSigUpView(BaseSigUpView):

    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        # create Dispatcher object in database
        dispatcher = Dispatcher()
        dispatcher.user_ptr = user
        dispatcher.user_ptr.user_type = 3
        dispatcher.user_ptr.save_base()
        dispatcher.save_base(raw=True)
        return user


class SendSMSCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format="json"):
        phone = request.data.get('phone')
        # if request.user.phone != phone:
        #     Response({'errors': ['Не верный номер телефона']}, status=status.HTTP_400_BAD_REQUEST)
        user = get_user_by_phone(phone)

        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        is_call = request.data.get('is_call')
        if is_call is not None:
            code = send_call(phone)
        else:
            code = send_sms(phone)
        return Response({'sms_code': code, 'uid': uid, 'token': token}, status=status.HTTP_200_OK)

