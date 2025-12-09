#SAmserv\models

from django.db import models

class Client(models.Model):
    phone_number = models.CharField('Телефон', max_length=20)
    email = models.CharField('Email', max_length=100)
    last_name = models.CharField('Фамилия', max_length=25)
    first_name = models.CharField('Имя', max_length=25)
    middle_name = models.CharField('Отчество', max_length=25, blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='clients/', blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Employee(models.Model):
    POSITION_CHOICES = [
        ('master', 'Мастер'),
        ('cashier', 'Кассир'),
        ('admin', 'Администратор'),
    ]
    
    last_name = models.CharField('Фамилия', max_length=25)
    first_name = models.CharField('Имя', max_length=25)
    middle_name = models.CharField('Отчество', max_length=25, blank=True, null=True)
    phone_number = models.CharField('Телефон', max_length=20)
    position = models.CharField('Должность', max_length=50, choices=POSITION_CHOICES)
    access_type = models.CharField('Доступ', max_length=20)
    photo = models.ImageField('Фото', upload_to='employees/', blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Device(models.Model):
    brand = models.CharField('Бренд', max_length=50)
    model = models.CharField('Модель', max_length=50)
    serial_number = models.CharField('Серийник', max_length=50)
    appearance = models.TextField('Внешний вид')
    photo = models.ImageField('Фото', upload_to='devices/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Service(models.Model):
    service_name = models.CharField('Услуга', max_length=100)
    service_cost = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.service_name

class Detail(models.Model):
    part_name = models.CharField('Деталь', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Количество')
    part_source = models.CharField('Источник', max_length=50)
    supplier = models.CharField('Поставщик', max_length=100)
    
    def __str__(self):
        return self.part_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('diagnostics', 'Диагностика'),
        ('repair', 'В ремонте'),
        ('ready', 'Готов'),
        ('issued', 'Выдан'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    master = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders_as_master', verbose_name='Мастер')
    services = models.ManyToManyField(Service, through='OrderService')
    details = models.ManyToManyField(Detail, through='OrderDetail')
    cashier = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders_as_cashier', verbose_name='Кассир')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    final_cost = models.DecimalField('Итоговая цена', max_digits=10, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    issue_description = models.TextField('Проблема')
    diagnosis = models.TextField('Диагностика', blank=True)
    estimated_cost = models.DecimalField('Предварительная цена', max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.client}"

class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('qr', 'QR-код'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_METHODS)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    
    def __str__(self):
        return f"Оплата заказа #{self.order.id}"
