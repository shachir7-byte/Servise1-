# SAMserv/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),

    path('clients/', views.client_list, name='client-list'),
    path('employees/', views.employee_list, name='employee-list'),
    path('devices/', views.device_list, name='device-list'),
    path('services/', views.service_list, name='service-list'),
    path('details/', views.detail_list, name='detail-list'),
]