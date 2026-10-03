import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db, get_connection
from routers import ingest, analytics
from services.json_processor import ingest_json
from services.xml_processor import ingest_xml
from services.csv_processor import ingest_csv

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def load_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    conn.close()

    json_path = os.path.join(DATA_DIR, "orders.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            ingest_json(json.load(f))

    csv_path = os.path.join(DATA_DIR, "products.csv")
    if os.path.exists(csv_path):
        with open(csv_path, "r") as f:
            ingest_csv(f.read())

    xml_path = os.path.join(DATA_DIR, "shipments.xml")
    if os.path.exists(xml_path):
        with open(xml_path, "r") as f:
            ingest_xml(f.read())


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    load_sample_data()
    yield


app = FastAPI(title="Full Stack Exercise API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, tags=["Ingest"])
app.include_router(analytics.router, tags=["Analytics"])


@app.get("/")
def root():
    return {"message": "Full Stack Exercise API is running"}
