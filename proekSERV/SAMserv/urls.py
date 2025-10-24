# SAMserv/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Заказы
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),

    # Клиенты
    path('clients/', views.client_list, name='client-list'),

    # Сотрудники
    path('employees/', views.employee_list, name='employee-list'),

    # Устройства
    path('devices/', views.device_list, name='device-list'),

    # Услуги
    path('services/', views.service_list, name='service-list'),

    # Запчасти
    path('details/', views.detail_list, name='detail-list'),
]