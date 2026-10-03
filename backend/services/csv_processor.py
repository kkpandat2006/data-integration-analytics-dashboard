import csv
import io
from db.database import get_connection


def ingest_csv(csv_string: str) -> dict:
    reader = csv.DictReader(io.StringIO(csv_string))
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for row in reader:
        pid = row.get("product_id", "").strip()
        if not pid:
            continue
        cursor.execute(
            "INSERT OR REPLACE INTO products (product_id, product_name, category) VALUES (?,?,?)",
            (pid, row.get("product_name", "").strip(), row.get("category", "").strip()),
        )
        count += 1

    conn.commit()
    conn.close()
    return {"products_inserted": count}
