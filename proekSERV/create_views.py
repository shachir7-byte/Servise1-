import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

view_sql = """
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
"""

cursor.executescript(view_sql)
conn.commit()
conn.close()
print("✅ Все VIEW успешно созданы!")
