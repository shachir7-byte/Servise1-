# SAMserv/views.py
from django.shortcuts import render, get_object_or_404
from .models import Order, Client, Employee, Device, Service, Detail

# --- Заказы ---
def order_list(request):
    orders = Order.objects.all().order_by('-created_date')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    services = order.orderservice_set.select_related('service').all()
    details = order.orderdetail_set.select_related('detail').all()
    payment = getattr(order, 'payment', None)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'services': services,
        'details': details,
        'payment': payment,
    })

# --- Клиенты ---
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

# --- Сотрудники ---
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

# --- Устройства ---
def device_list(request):
    devices = Device.objects.all()
    return render(request, 'devices/device_list.html', {'devices': devices})

# --- Услуги ---
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

# --- Запчасти ---
def detail_list(request):
    details = Detail.objects.all()
    return render(request, 'details/detail_list.html', {'details': details})

#views/samserv