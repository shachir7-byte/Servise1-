from django.shortcuts import render, get_object_or_404
from .models import Order

def order_list(request):
    orders = Order.objects.all().order_by('-created_date')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    services = order.orderservice_set.select_related('service').all()
    details = order.orderdetail_set.select_related('detail').all()
    payment = getattr(order, 'payment', None)  # безопасно, если оплаты нет

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'services': services,
        'details': details,
        'payment': payment,
    })