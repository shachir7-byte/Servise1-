from django.db import models

# ... остальные импорты ...

class Client(models.Model):
    # ... существующие поля ...
    photo = models.ImageField(upload_to='clients/', blank=True, null=True)

class Employee(models.Model):
    # ... существующие поля ...
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)

class Device(models.Model):
    # ... существующие поля ...
    photo = models.ImageField(upload_to='devices/', blank=True, null=True)

class YourModel(models.Model):
    name = models.CharField(max_length=100)
    # Поле для загрузки изображений
    photo = models.ImageField(upload_to='uploads/photos/')  # Файлы будут сохраняться в media/uploads/photos/
    # Поле для загрузки любых файлов
    document = models.FileField(upload_to='uploads/documents/')

    
class Client(models.Model):
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Employee(models.Model):
    POSITION_CHOICES = [
        ('master', 'Мастер'),
        ('cashier', 'Кассир'),
        ('admin', 'Администратор'),
    ]
    
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    access_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"

class Device(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    appearance = models.TextField()
    
    def __str__(self):
        return f"{self.brand} {self.model}"

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.service_name

class Detail(models.Model):
    part_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    part_source = models.CharField(max_length=50)
    supplier = models.CharField(max_length=100)
    
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
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    master = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders_as_master')
    services = models.ManyToManyField(Service, through='OrderService')
    details = models.ManyToManyField(Detail, through='OrderDetail')
    cashier = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders_as_cashier')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    issue_description = models.TextField()
    diagnosis = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    
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
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Оплата заказа #{self.order.id}"
    
    #models/samserv