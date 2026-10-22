import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "data_integration_db"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


def init_db():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id VARCHAR(100) PRIMARY KEY,
                    customer_id VARCHAR(100),
                    customer_name VARCHAR(255),
                    order_date VARCHAR(50)
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id VARCHAR(100) PRIMARY KEY,
                    product_name VARCHAR(255),
                    category VARCHAR(100)
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id VARCHAR(100),
                    product_id VARCHAR(100),
                    qty INT,
                    price DOUBLE,
                    line_total DOUBLE,
                    FOREIGN KEY (order_id)
                        REFERENCES orders(order_id)
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    shipment_id VARCHAR(100) PRIMARY KEY,
                    order_id VARCHAR(100),
                    delivery_days INT,
                    status VARCHAR(100),
                    FOREIGN KEY (order_id)
                        REFERENCES orders(order_id)
                ) ENGINE=InnoDB
            """)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()