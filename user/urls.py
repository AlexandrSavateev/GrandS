from django.urls import path, include
from django.conf import settings
from user.views.auth import *
from user.views.social import *
from user.views.details import *


social_urlpatterns = [
    path('google/client/private/', ClientPrivateGoogleLogin.as_view(), name='client-private-google-login'),
    path('google/client/legal/', ClientLegalGoogleLogin.as_view(), name='client-legal-google-login'),
    path('google/dispatcher/', DispatcherGoogleLogin.as_view(), name='dispatcher-google-login'),
    path('facebook/client/private/', ClientPrivateFacebookLogin.as_view(), name='client-private-facebook-login'),
    path('facebook/client/legal/', ClientLegalFacebookLogin.as_view(), name='client-legal-facebook-login'),
    path('facebook/dispatcher/', DispatcherFacebookLogin.as_view(), name='dispatcher-facebook-login'),
    # to allow connecting existing accounts in addition to login
    # path('facebook/connect/', GoogleConnect.as_view(), name='fb-connect'),
    # path('twitter/connect/', FacebookConnect.as_view(), name='twitter-connect'),
]

rest_auth_urlpatterns = [
    path('', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('social/', include(social_urlpatterns)),
    # path('registration/base/', views.BaseSigUpView.as_view(), name='base-signup'),
    path('registration/client/private/', ClientPrivateSigUpView.as_view(), name='client-private-signup'),
    path('registration/client/legal/', ClientLegalSigUpView.as_view(), name='client-signup'),
    path('registration/dispatcher/', DispatcherSigUpView.as_view(), name='dispatcher-signup'),
    path('send-sms/', SendSMSCodeView.as_view(), name='send-sms'),
    path('user/client/private/', ClientPrivateDetailsView.as_view(), name='client-private-details'),
    path('user/client/legal/', ClientLegalDetailsView.as_view(), name='client-legal-details'),
    path('user/dispatcher/', DispatcherDetailsView.as_view(), name='dispatcher-details'),
    path('user/drivers/', DriverByDispatcherList.as_view({'get': 'list'})),
    path('user/drivers/<int:pk>/', DriverByDispatcherDetail.as_view()),
]

urlpatterns = [
    path('rest-auth/', include(rest_auth_urlpatterns)),
]

# if settings.DEBUG:
#     from django.views.generic import TemplateView
#
#     test_urlpatterns = [
#         path('test_profile/', views.WelcomeView.as_view(), name='welcome'),
#         path('test_profile/social/', TemplateView.as_view(template_name="login_social.html")),
#     ]
#     urlpatterns += test_urlpatterns
