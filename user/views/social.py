from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView

from user.models import ClientPrivate, ClientLegal, Dispatcher
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class CustomSocialLoginView(SocialLoginView):
    user_profile = UserModel

    def get_response(self):
        # Override rest_auth.views.LoginView method

        # Create appropriate user profile
        profile = self.user_profile()
        profile.user_ptr = self.user
        profile.save_base(raw=True)

        resp = super().get_response()

        # send sms logic if necessary
        # resp.data.update(sms_code=code)

        return resp


class ClientPrivateGoogleLogin(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    user_profile = ClientPrivate


class ClientLegalGoogleLogin(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    user_profile = ClientLegal


class DispatcherGoogleLogin(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    user_profile = Dispatcher


class ClientPrivateFacebookLogin(CustomSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    user_profile = ClientPrivate


class ClientLegalFacebookLogin(CustomSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    user_profile = ClientLegal


class DispatcherFacebookLogin(CustomSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    user_profile = Dispatcher
