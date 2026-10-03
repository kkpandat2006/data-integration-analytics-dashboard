from typing import Optional
from db.database import get_connection


def get_joined_data(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    category: Optional[str] = None,
    delivery_status: Optional[str] = None,
) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            o.order_id, o.customer_id, o.customer_name, o.order_date,
            oi.product_id, oi.qty, oi.price, oi.line_total,
            p.product_name, p.category,
            s.shipment_id, s.delivery_days, s.status AS delivery_status,
            CASE WHEN s.status = 'Delayed' THEN 1 ELSE 0 END AS delay_flag
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN products p    ON oi.product_id = p.product_id
        LEFT JOIN shipments s   ON o.order_id = s.order_id
        WHERE 1=1
    """
    params: list = []
    if date_from:
        query += " AND o.order_date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND o.order_date <= ?"
        params.append(date_to)
    if category:
        query += " AND p.category = ?"
        params.append(category)
    if delivery_status:
        query += " AND s.status = ?"
        params.append(delivery_status)

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_analytics_summary(
    date_from=None, date_to=None, category=None, delivery_status=None,
    page=1, page_size=10, target_currency=None,
) -> dict:
    from services.currency_service import convert_amount

    data = get_joined_data(date_from, date_to, category, delivery_status)
    rate = convert_amount(1.0, "USD", target_currency) if target_currency else 1.0

    order_ids = {r["order_id"] for r in data if r.get("order_id")}
    total_revenue = round(sum(r.get("line_total") or 0 for r in data) * rate, 2)
    delayed_ids = {r["order_id"] for r in data if r.get("delivery_status") == "Delayed"}

    cat_rev, cat_ord = {}, {}
    for r in data:
        cat = r.get("category") or "Unknown"
        cat_rev[cat] = cat_rev.get(cat, 0) + (r.get("line_total") or 0)
        cat_ord.setdefault(cat, set()).add(r.get("order_id"))
    categories = [
        {"category": c, "revenue": round(cat_rev[c] * rate, 2), "order_count": len(cat_ord[c])}
        for c in cat_rev
    ]

    del_map: dict = {}
    for r in data:
        s = r.get("delivery_status") or "Unknown"
        del_map[s] = del_map.get(s, 0) + 1
    delivery_performance = [{"status": k, "count": v} for k, v in del_map.items()]

    trend: dict = {}
    for r in data:
        d = r.get("order_date") or "Unknown"
        trend.setdefault(d, {"revenue": 0, "orders": set()})
        trend[d]["revenue"] += r.get("line_total") or 0
        trend[d]["orders"].add(r.get("order_id"))
    revenue_trend = [
        {"date": d, "revenue": round(trend[d]["revenue"] * rate, 2), "order_count": len(trend[d]["orders"])}
        for d in sorted(trend)
    ]

    order_map: dict = {}
    for r in data:
        oid = r["order_id"]
        if oid not in order_map:
            order_map[oid] = {
                "order_id": oid, "customer_name": r.get("customer_name"),
                "order_date": r.get("order_date"), "total_value": 0.0,
                "delivery_status": r.get("delivery_status"),
                "delay_flag": bool(r.get("delay_flag")), "items": [],
            }
        order_map[oid]["total_value"] += r.get("line_total") or 0
        order_map[oid]["items"].append({
            "product_id": r.get("product_id"), "product_name": r.get("product_name"),
            "category": r.get("category"), "qty": r.get("qty"),
            "price": r.get("price"), "line_total": r.get("line_total"),
        })
    for o in order_map.values():
        o["total_value"] = round(o["total_value"] * rate, 2)
        for it in o["items"]:
            it["price"] = round((it["price"] or 0) * rate, 2)
            it["line_total"] = round((it["line_total"] or 0) * rate, 2)

    orders_list = list(order_map.values())

    total_items = len(orders_list)
    total_pages = max(1, -(-total_items // page_size))
    start = (page - 1) * page_size
    paginated = orders_list[start : start + page_size]

    return {
        "total_orders": len(order_ids),
        "total_revenue": total_revenue,
        "delayed_orders": len(delayed_ids),
        "categories": categories,
        "delivery_performance": delivery_performance,
        "revenue_trend": revenue_trend,
        "orders": paginated,
        "pagination": {"page": page, "page_size": page_size, "total_items": total_items, "total_pages": total_pages},
    }
