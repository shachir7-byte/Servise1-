# SAMserv/views.py
# САМЫЙ ПРОСТОЙ И РАБОЧИЙ ВАРИАНТ ДЛЯ 3 КУРСА
# Поиск работает и на "Иван", и на "иван", и на "ИВАН" без всяких COLIATE и Lower()

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Order, Client, Employee, Device, Service, Detail


def client_list(request):
    query = request.GET.get('q', '').strip()
    clients = Client.objects.all().order_by('last_name')

    if query:
        clients = clients.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'clients/client_list.html', {'clients': clients, 'query': query})


def employee_list(request):
    query = request.GET.get('q', '').strip()
    employees = Employee.objects.all().order_by('last_name')

    if query:
        employees = employees.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(position__icontains=query)
        )

    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})


def order_list(request):
    query = request.GET.get('q', '').strip()
    orders = Order.objects.select_related('client', 'device', 'master').all().order_by('-created_date')

    if query:
        if query.isdigit():
            orders = orders.filter(id=int(query))
        else:
            orders = orders.filter(
                Q(client__last_name__icontains=query) |
                Q(client__first_name__icontains=query) |
                Q(device__brand__icontains=query) |
                Q(device__model__icontains=query) |
                Q(issue_description__icontains=query)
            )

    return render(request, 'orders/order_list.html', {'orders': orders, 'query': query})


def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('client', 'device', 'master', 'cashier'), pk=pk)
    services = order.orderservice_set.select_related('service').all()
    details = order.orderdetail_set.select_related('detail').all()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'services': services,
        'details': details,
    })


def device_list(request):
    query = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '')
    model = request.GET.get('model', '')

    devices = Device.objects.all()

    if query:
        devices = devices.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(serial_number__icontains=query)
        )
    if brand:
        devices = devices.filter(brand__icontains=brand)
    if model:
        devices = devices.filter(model__icontains=model)

    brands = Device.objects.values_list('brand', flat=True).distinct().order_by('brand')
    models = Device.objects.values_list('model', flat=True).distinct().order_by('model')

    return render(request, 'devices/device_list.html', {
        'devices': devices,
        'brands': brands,
        'models': models,
        'query': query,
        'selected_brand': brand,
        'selected_model': model,
    })


def service_list(request):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    services = Service.objects.all().order_by('service_name')

    if query:
        services = services.filter(service_name__icontains=query)
    if min_price:
        try:
            services = services.filter(service_cost__gte=float(min_price))
        except:
            pass
    if max_price:
        try:
            services = services.filter(service_cost__lte=float(max_price))
        except:
            pass

    return render(request, 'services/service_list.html', {
        'services': services,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    })


def detail_list(request):
    query = request.GET.get('q', '').strip()
    details = Detail.objects.all().order_by('part_name')

    if query:
        details = details.filter(
            Q(part_name__icontains=query) |
            Q(supplier__icontains=query)
        )

    return render(request, 'details/detail_list.html', {'details': details, 'query': query})