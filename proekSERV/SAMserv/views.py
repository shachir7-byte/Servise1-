# SAMserv/views.py
from django.shortcuts import render, get_object_or_404
from .models import Order, Client, Employee, Device, Service, Detail

def order_list(request):
    orders = Order.objects.select_related('client', 'device').all()  # меньше запросов к БД
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('client', 'device', 'master', 'cashier'), pk=pk)
    services = order.orderservice_set.select_related('service').all()  # оптимизация
    details = order.orderdetail_set.select_related('detail').all()     # оптимизация
    payment = getattr(order, 'payment', None)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'services': services,
        'details': details,
        'payment': payment,
    })

def client_list(request):
    clients = Client.objects.all().order_by('last_name')
    return render(request, 'clients/client_list.html', {'clients': clients})

def employee_list(request):
    employees = Employee.objects.all().order_by('last_name')
    return render(request, 'employees/employee_list.html', {'employees': employees})

def device_list(request):
    devices = Device.objects.all().order_by('brand')
    return render(request, 'devices/device_list.html', {'devices': devices})

def service_list(request):
    services = Service.objects.all().order_by('service_name')
    return render(request, 'services/service_list.html', {'services': services})

def detail_list(request):
    details = Detail.objects.all().order_by('part_name')
    return render(request, 'details/detail_list.html', {'details': details})