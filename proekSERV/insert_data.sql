-- Заполняем клиентов
INSERT INTO SAMserv_client (phone_number, email, last_name, first_name, middle_name, photo)
VALUES 
('89001234567', 'ivanov@mail.ru', 'Иванов', 'Иван', 'Иванович', 'clients/ivanov.jpg'),
('89007654321', 'petrov@mail.ru', 'Петров', 'Пётр', 'Сергеевич', 'clients/petrov.jpg');

-- Заполняем сотрудников
INSERT INTO SAMserv_employee (last_name, first_name, middle_name, phone_number, position, access_type, photo)
VALUES 
('Сидоров', 'Андрей', 'Владимирович', '89001112233', 'master', 'full', 'employees/sidorov.jpg'),
('Козлова', 'Мария', 'Петровна', '89004445566', 'cashier', 'limited', 'employees/kozlova.jpg');

-- Заполняем устройства
INSERT INTO SAMserv_device (brand, model, serial_number, appearance, photo)
VALUES 
('Apple', 'iPhone 15 Pro', 'SN123456789', 'Царапина на экране', 'devices/iphone15.jpg'),
('Samsung', 'Galaxy S24', 'SN987654321', 'Разбитый корпус', 'devices/samsungs24.jpg');

-- Заполняем услуги
INSERT INTO SAMserv_service (service_name, service_cost)
VALUES 
('Замена дисплея', 5000.00),
('Замена аккумулятора', 2500.00);

-- Заполняем детали
INSERT INTO SAMserv_detail (part_name, price, quantity, part_source, supplier)
VALUES 
('Дисплей iPhone 15 Pro', 4000.00, 10, 'Оптовик', 'TechParts Inc.'),
('Аккумулятор Samsung S24', 1500.00, 5, 'Завод', 'Samsung OEM');

-- Заполняем заказы
INSERT INTO SAMserv_order (client_id, device_id, master_id, cashier_id, status, final_cost, created_date, issue_description, diagnosis, estimated_cost)
VALUES 
(1, 1, 1, 2, 'ready', 5000.00, '2025-12-01 10:00:00', 'Не включается', 'Неисправен дисплей', 5000.00),
(2, 2, 1, 2, 'issued', 2500.00, '2025-12-02 14:30:00', 'Быстро разряжается', 'Неисправен аккумулятор', 2500.00);

-- Заполняем OrderService
INSERT INTO SAMserv_orderservice (order_id, service_id, quantity)
VALUES 
(1, 1, 1),
(2, 2, 1);

-- Заполняем OrderDetail
INSERT INTO SAMserv_orderdetail (order_id, detail_id, quantity)
VALUES 
(1, 1, 1),
(2, 2, 1);

-- Заполняем Payment
INSERT INTO SAMserv_payment (order_id, payment_method, amount, payment_date)
VALUES 
(1, 'card', 5000.00, '2025-12-01 11:00:00'),
(2, 'cash', 2500.00, '2025-12-02 15:00:00');