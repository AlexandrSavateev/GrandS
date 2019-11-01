"""
gt URL Configuration

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from core.views.order import PaymentsNotificationView, OrderPaymentView, PaymentsReturnsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/payments/<str: status>/', PaymentsReturnsView.as_view()),
    path('orders/payments/notifications/', PaymentsNotificationView.as_view()),
    path('orders/<int:pk>/payment/', OrderPaymentView.as_view()),
    path('api/', include('user.urls')),
    path('api/technics/', include('core.urls.technics')),
    path('api/orders/', include('core.urls.order'))
]
