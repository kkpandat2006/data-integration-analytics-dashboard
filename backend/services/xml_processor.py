import xml.etree.ElementTree as ET
from db.database import get_connection


def ingest_xml(xml_string: str) -> dict:
    root = ET.fromstring(xml_string)
    conn = get_connection()
    count = 0

    try:
        with conn.cursor() as cursor:
            for shipment in root.findall("shipment"):
                sid = shipment.findtext("shipment_id", "").strip()
                oid = shipment.findtext("order_id", "").strip()
                days = int(shipment.findtext("delivery_days", "0"))
                status = shipment.findtext("status", "").strip()

                if not sid:
                    continue

                cursor.execute(
                    """
                    INSERT INTO shipments
                        (shipment_id, order_id, delivery_days, status)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        order_id = VALUES(order_id),
                        delivery_days = VALUES(delivery_days),
                        status = VALUES(status)
                    """,
                    (sid, oid, days, status),
                )

                count += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return {"shipments_inserted": count}