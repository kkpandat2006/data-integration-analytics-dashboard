
from typing import Optional

from db.database import get_connection


def get_joined_data(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    category: Optional[str] = None,
    delivery_status: Optional[str] = None,
) -> list:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    o.order_id,
                    o.customer_id,
                    o.customer_name,
                    o.order_date,
                    oi.product_id,
                    oi.qty,
                    oi.price,
                    oi.line_total,
                    p.product_name,
                    p.category,
                    s.shipment_id,
                    s.delivery_days,
                    s.status AS delivery_status,
                    CASE
                        WHEN s.status = 'Delayed' THEN 1
                        ELSE 0
                    END AS delay_flag
                FROM orders o
                LEFT JOIN order_items oi
                    ON o.order_id = oi.order_id
                LEFT JOIN products p
                    ON oi.product_id = p.product_id
                LEFT JOIN shipments s
                    ON o.order_id = s.order_id
                WHERE 1=1
            """

            params = []

            if date_from:
                query += " AND o.order_date >= %s"
                params.append(date_from)

            if date_to:
                query += " AND o.order_date <= %s"
                params.append(date_to)

            if category:
                query += " AND p.category = %s"
                params.append(category)

            if delivery_status:
                query += " AND s.status = %s"
                params.append(delivery_status)

            cursor.execute(query, params)
            rows = [dict(row) for row in cursor.fetchall()]

        return rows

    finally:
        conn.close()


def get_analytics_summary(
    date_from=None,
    date_to=None,
    category=None,
    delivery_status=None,
    page=1,
    page_size=10,
    target_currency=None,
) -> dict:
    from services.currency_service import convert_amount

    data = get_joined_data(
        date_from=date_from,
        date_to=date_to,
        category=category,
        delivery_status=delivery_status,
    )

    rate = (
        convert_amount(1.0, "USD", target_currency)
        if target_currency
        else 1.0
    )

    order_ids = {
        row["order_id"]
        for row in data
        if row.get("order_id")
    }

    total_revenue = round(
        sum(row.get("line_total") or 0 for row in data) * rate,
        2,
    )

    delayed_ids = {
        row["order_id"]
        for row in data
        if row.get("delivery_status") == "Delayed"
    }

    # Category-wise revenue and order count
    category_revenue = {}
    category_orders = {}

    for row in data:
        category_name = row.get("category") or "Unknown"
        order_id = row.get("order_id")

        category_revenue[category_name] = (
            category_revenue.get(category_name, 0)
            + (row.get("line_total") or 0)
        )

        category_orders.setdefault(category_name, set()).add(order_id)

    categories = [
        {
            "category": category_name,
            "revenue": round(category_revenue[category_name] * rate, 2),
            "order_count": len(category_orders[category_name]),
        }
        for category_name in category_revenue
    ]

    # Delivery performance
    delivery_map = {}

    for row in data:
        status = row.get("delivery_status") or "Unknown"
        delivery_map[status] = delivery_map.get(status, 0) + 1

    delivery_performance = [
        {"status": status, "count": count}
        for status, count in delivery_map.items()
    ]

    # Revenue trend
    trend = {}

    for row in data:
        order_date = row.get("order_date") or "Unknown"

        trend.setdefault(
            order_date,
            {"revenue": 0, "orders": set()},
        )

        trend[order_date]["revenue"] += row.get("line_total") or 0
        trend[order_date]["orders"].add(row.get("order_id"))

    revenue_trend = [
        {
            "date": order_date,
            "revenue": round(trend[order_date]["revenue"] * rate, 2),
            "order_count": len(trend[order_date]["orders"]),
        }
        for order_date in sorted(trend)
    ]

    # Order-wise details
    order_map = {}

    for row in data:
        order_id = row["order_id"]

        if order_id not in order_map:
            order_map[order_id] = {
                "order_id": order_id,
                "customer_name": row.get("customer_name"),
                "order_date": row.get("order_date"),
                "total_value": 0.0,
                "delivery_status": row.get("delivery_status"),
                "delay_flag": bool(row.get("delay_flag")),
                "items": [],
            }

        order_map[order_id]["total_value"] += (
            row.get("line_total") or 0
        )

        # LEFT JOIN ke kaaran item details missing ho sakti hain.
        if row.get("product_id") is not None:
            order_map[order_id]["items"].append(
                {
                    "product_id": row.get("product_id"),
                    "product_name": row.get("product_name"),
                    "category": row.get("category"),
                    "qty": row.get("qty"),
                    "price": row.get("price"),
                    "line_total": row.get("line_total"),
                }
            )

    for order in order_map.values():
        order["total_value"] = round(
            order["total_value"] * rate,
            2,
        )

        for item in order["items"]:
            item["price"] = round(
                (item["price"] or 0) * rate,
                2,
            )

            item["line_total"] = round(
                (item["line_total"] or 0) * rate,
                2,
            )

    orders_list = list(order_map.values())

    # Pagination
    total_items = len(orders_list)
    page_size = max(1, int(page_size))
    page = max(1, int(page))

    total_pages = max(
        1,
        -(-total_items // page_size),
    )

    start = (page - 1) * page_size
    paginated_orders = orders_list[start:start + page_size]

    return {
        "total_orders": len(order_ids),
        "total_revenue": total_revenue,
        "delayed_orders": len(delayed_ids),
        "categories": categories,
        "delivery_performance": delivery_performance,
        "revenue_trend": revenue_trend,
        "orders": paginated_orders,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        },
    }
