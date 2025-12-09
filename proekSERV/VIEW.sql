--D:\vsCODE\proektiki\Servise1-\proekSERV\VIEW.sql

-- database: /path/to/database.db
-- VIEW 1: Сводка по заказам (клиент + устройство + статус)
CREATE VIEW IF NOT EXISTS order_summary AS
SELECT
    o.id AS order_id,
    c.last_name || ' ' || c.first_name AS client_name,
    d.brand || ' ' || d.model AS device,
    o.status,
    o.created_date,
    o.final_cost
FROM SAMserv_order o
JOIN SAMserv_client c ON o.client_id = c.id
JOIN SAMserv_device d ON o.device_id = d.id;

-- VIEW 2: Используемые услуги в заказах
CREATE VIEW IF NOT EXISTS order_services_detail AS
SELECT
    o.id AS order_id,
    c.last_name AS client_last_name,
    s.service_name,
    os.quantity,
    s.service_cost,
    (os.quantity * s.service_cost) AS total_service_cost
FROM SAMserv_order o
JOIN SAMserv_client c ON o.client_id = c.id
JOIN SAMserv_orderservice os ON o.id = os.order_id
JOIN SAMserv_service s ON os.service_id = s.id;

-- VIEW 3: Используемые детали в заказах
CREATE VIEW IF NOT EXISTS order_details_used AS
SELECT
    o.id AS order_id,
    d.part_name,
    od.quantity,
    d.price,
    (od.quantity * d.price) AS total_detail_cost
FROM SAMserv_order o
JOIN SAMserv_orderdetail od ON o.id = od.order_id
JOIN SAMserv_detail d ON od.detail_id = d.id;