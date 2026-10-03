from db.database import get_connection


def ingest_json(data: dict) -> dict:
    orders = data.get("orders", [])
    conn = get_connection()
    cursor = conn.cursor()

    orders_count = 0
    items_count = 0

    for order in orders:
        order_id = str(order.get("order_id", "")).strip()
        if not order_id:
            continue

        customer = order.get("customer", {})
        cursor.execute(
            "INSERT OR REPLACE INTO orders (order_id, customer_id, customer_name, order_date) VALUES (?,?,?,?)",
            (order_id, str(customer.get("id", "")), str(customer.get("name", "")), order.get("order_date", "")),
        )
        orders_count += 1

        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))

        for item in order.get("items", []):
            qty = int(item.get("qty", 0))
            price = float(item.get("price", 0))
            line_total = round(qty * price, 2)
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, qty, price, line_total) VALUES (?,?,?,?,?)",
                (order_id, str(item.get("product_id", "")).strip(), qty, price, line_total),
            )
            items_count += 1

    conn.commit()
    conn.close()
    return {"orders_inserted": orders_count, "items_inserted": items_count}
