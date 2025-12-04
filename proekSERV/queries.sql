-- 1. Простой SELECT
SELECT * FROM SAMserv_client WHERE last_name = 'Иванов';

-- 2. JOIN по 3 таблицам
SELECT 
    o.id AS order_id,
    c.last_name || ' ' || c.first_name AS client,
    d.brand || ' ' || d.model AS device,
    o.status
FROM SAMserv_order o
JOIN SAMserv_client c ON o.client_id = c.id
JOIN SAMserv_device d ON o.device_id = d.id;

-- 3. Агрегация: количество заказов по статусу
SELECT status, COUNT(*) AS count
FROM SAMserv_order
GROUP BY status;

-- 4. Подзапрос: заказы клиентов с email @gmail.com
SELECT o.*
FROM SAMserv_order o
WHERE o.client_id IN (
    SELECT id FROM SAMserv_client WHERE email LIKE '%@gmail.com'
);