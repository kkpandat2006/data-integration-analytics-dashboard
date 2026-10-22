import csv
import io
from db.database import get_connection


def ingest_csv(csv_string: str) -> dict:
    reader = csv.DictReader(io.StringIO(csv_string))
    conn = get_connection()
    count = 0

    try:
        with conn.cursor() as cursor:
            for row in reader:
                pid = row.get("product_id", "").strip()

                if not pid:
                    continue

                cursor.execute(
                    """
                    INSERT INTO products
                        (product_id, product_name, category)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        product_name = VALUES(product_name),
                        category = VALUES(category)
                    """,
                    (
                        pid,
                        row.get("product_name", "").strip(),
                        row.get("category", "").strip(),
                    ),
                )
                count += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return {"products_inserted": count}