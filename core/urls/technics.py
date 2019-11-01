from django.urls import path, include
from ..views.technics import CategoryView, AutoByDispatcherList, AutoByDispatcherDetail
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('catalog/', CategoryView.as_view()),
    path('autos/', AutoByDispatcherList.as_view({'get': 'get', 'post': 'create'})),
    path('autos/<int:pk>/', AutoByDispatcherDetail.as_view())
]