#SAMserv/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Client, Employee, Device, Service, Detail, Order, Payment, OrderService, OrderDetail

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'phone_number', 'email', 'photo_preview']
    search_fields = ['last_name', 'first_name', 'phone_number', 'email']
    list_filter = ['last_name']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Фото'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'position', 'phone_number']
    list_filter = ['position']
    search_fields = ['last_name', 'first_name', 'phone_number']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'serial_number', 'photo_preview']
    search_fields = ['brand', 'model', 'serial_number']
    list_filter = ['brand']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Фото'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_cost']
    list_filter = ['service_cost']
    search_fields = ['service_name']

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'price', 'quantity', 'supplier']
    list_filter = ['supplier', 'quantity']
    search_fields = ['part_name', 'supplier']

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 1

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'device', 'status', 'created_date', 'final_cost']
    list_filter = ['status', 'created_date', 'client__last_name']
    search_fields = ['client__last_name', 'device__brand', 'id']
    inlines = [OrderServiceInline, OrderDetailInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'payment_date']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['order__id']
