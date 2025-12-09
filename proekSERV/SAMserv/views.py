# SAMserv/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Func
from .models import Order, Client, Employee, Device, Service, Detail

class Lower(Func):
    function = 'LOWER'

def order_list(request):
    query = request.GET.get('q')
    orders = Order.objects.select_related('client', 'device').all()

    if query:
        try:
            # Поиск по ID заказа
            order_id = int(query)
            orders = orders.filter(id=order_id)
        except ValueError:
            # Если не число, ищем по клиенту и устройству
            orders = orders.filter(
                Q(client__first_name__icontains=query) |
                Q(client__last_name__icontains=query) |
                Q(device__brand__icontains=query) |
                Q(device__model__icontains=query)
            )

    return render(request, 'orders/order_list.html', {'orders': orders, 'query': query})

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
    query = request.GET.get('q')
    print(f"[DEBUG] Запрос: '{query}'")  # 👈 Добавь это
    clients = Client.objects.all().order_by('last_name')

    if query:
        clients = clients.annotate(
            first_name_lower=Lower('first_name'),
            last_name_lower=Lower('last_name'),
            phone_number_lower=Lower('phone_number'),
            email_lower=Lower('email')
        ).filter(
            Q(first_name_lower__contains=query.lower()) |
            Q(last_name_lower__contains=query.lower()) |
            Q(phone_number_lower__contains=query.lower()) |
            Q(email_lower__contains=query.lower())
        )
        print(f"[DEBUG] Найдено клиентов: {clients.count()}")  # 👈 И это

    return render(request, 'clients/client_list.html', {'clients': clients, 'query': query})

def employee_list(request):
    query = request.GET.get('q')
    employees = Employee.objects.all().order_by('last_name')

    if query:
        employees = employees.annotate(
            first_name_lower=Lower('first_name'),
            last_name_lower=Lower('last_name'),
            phone_number_lower=Lower('phone_number'),
            position_lower=Lower('position')
        ).filter(
            Q(first_name_lower__contains=query.lower()) |
            Q(last_name_lower__contains=query.lower()) |
            Q(phone_number_lower__contains=query.lower()) |
            Q(position_lower__contains=query.lower())
        )

    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})

def device_list(request):
    query = request.GET.get('q')
    brand_filter = request.GET.get('brand')
    model_filter = request.GET.get('model')

    devices = Device.objects.all().order_by('brand')

    if query:
        devices = devices.annotate(
            brand_lower=Lower('brand'),
            model_lower=Lower('model'),
            serial_number_lower=Lower('serial_number')
        ).filter(
            Q(brand_lower__contains=query.lower()) |
            Q(model_lower__contains=query.lower()) |
            Q(serial_number_lower__contains=query.lower())
        )
    if brand_filter:
        devices = devices.filter(brand__icontains=brand_filter)
    if model_filter:
        devices = devices.filter(model__icontains=model_filter)

    # Для фильтров в шаблоне
    brands = Device.objects.values_list('brand', flat=True).distinct()
    models = Device.objects.values_list('model', flat=True).distinct()

    return render(request, 'devices/device_list.html', {
        'devices': devices,
        'brands': brands,
        'models': models,
        'selected_brand': brand_filter,
        'selected_model': model_filter,
        'query': query,
    })

def service_list(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    services = Service.objects.all().order_by('service_name')

    if query:
        services = services.annotate(
            service_name_lower=Lower('service_name')
        ).filter(
            service_name_lower__contains=query.lower()
        )
    if min_price:
        try:
            min_price = float(min_price)
            services = services.filter(service_cost__gte=min_price)
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            max_price = float(max_price)
            services = services.filter(service_cost__lte=max_price)
        except (ValueError, TypeError):
            pass

    return render(request, 'services/service_list.html', {
        'services': services,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    })

def detail_list(request):
    query = request.GET.get('q')
    supplier_filter = request.GET.get('supplier')
    min_quantity = request.GET.get('min_quantity')
    max_quantity = request.GET.get('max_quantity')

    details = Detail.objects.all().order_by('part_name')

    if query:
        details = details.annotate(
            part_name_lower=Lower('part_name'),
            supplier_lower=Lower('supplier'),
            part_source_lower=Lower('part_source')
        ).filter(
            Q(part_name_lower__contains=query.lower()) |
            Q(supplier_lower__contains=query.lower()) |
            Q(part_source_lower__contains=query.lower())
        )
    if supplier_filter:
        details = details.filter(supplier__icontains=supplier_filter)
    if min_quantity:
        try:
            min_quantity = int(min_quantity)
            details = details.filter(quantity__gte=min_quantity)
        except (ValueError, TypeError):
            pass
    if max_quantity:
        try:
            max_quantity = int(max_quantity)
            details = details.filter(quantity__lte=max_quantity)
        except (ValueError, TypeError):
            pass

    suppliers = Detail.objects.values_list('supplier', flat=True).distinct()

    return render(request, 'details/detail_list.html', {
        'details': details,
        'suppliers': suppliers,
        'query': query,
        'min_quantity': min_quantity,
        'max_quantity': max_quantity,
        'selected_supplier': supplier_filter,
    })