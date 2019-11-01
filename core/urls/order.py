from django.urls import path, include
from ..views.order import OrderList, SearchOrderList, OrderDetail, \
    CreatePointView, CreateTechicsView, CreateImagesView, ConfirmOrderView, get_calendar
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('', OrderList.as_view({'get': 'list', 'post': 'create'})),
    path('search/', SearchOrderList.as_view({'post': 'search'})),
    path('<int:pk>/', OrderDetail.as_view()),
    path('<int:pk>/points/', CreatePointView.as_view({'post': 'post'})),
    path('<int:pk>/technics/', CreateTechicsView.as_view({'post': 'post'})),
    path('<int:pk>/images/', CreateImagesView.as_view({'post': 'post'})),
    path('<int:pk>/confirm/', ConfirmOrderView.as_view()),

]