from django.contrib import admin
from .models import Client, Employee, Device, Service, Detail, Order, Payment, OrderService, OrderDetail

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'phone_number', 'email']
    search_fields = ['last_name', 'first_name', 'phone_number']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'position', 'phone_number']
    list_filter = ['position']
    search_fields = ['last_name', 'first_name']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'serial_number']
    search_fields = ['brand', 'model', 'serial_number']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_cost']
    list_filter = ['service_cost']

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'price', 'quantity', 'supplier']
    list_filter = ['supplier']
    search_fields = ['part_name']

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 1

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'device', 'status', 'created_date', 'final_cost']
    list_filter = ['status', 'created_date']
    search_fields = ['client__last_name', 'device__brand']
    inlines = [OrderServiceInline, OrderDetailInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'payment_date']
    list_filter = ['payment_method', 'payment_date']

#admin/samserv