import xml.etree.ElementTree as ET
from db.database import get_connection


def ingest_xml(xml_string: str) -> dict:
    root = ET.fromstring(xml_string)
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for shipment in root.findall("shipment"):
        sid = shipment.findtext("shipment_id", "").strip()
        oid = shipment.findtext("order_id", "").strip()
        days = int(shipment.findtext("delivery_days", "0"))
        status = shipment.findtext("status", "").strip()
        if not sid:
            continue
        cursor.execute(
            "INSERT OR REPLACE INTO shipments (shipment_id, order_id, delivery_days, status) VALUES (?,?,?,?)",
            (sid, oid, days, status),
        )
        count += 1

    conn.commit()
    conn.close()
    return {"shipments_inserted": count}
