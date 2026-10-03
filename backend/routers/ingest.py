from fastapi import APIRouter, Request, HTTPException
from models.schemas import IngestResponse
from services.json_processor import ingest_json
from services.xml_processor import ingest_xml
from services.csv_processor import ingest_csv

router = APIRouter()


@router.post("/ingest/json", response_model=IngestResponse)
async def ingest_json_endpoint(request: Request):
    try:
        body = await request.json()
        result = ingest_json(body)
        return IngestResponse(success=True, message="JSON data ingested", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ingest/xml", response_model=IngestResponse)
async def ingest_xml_endpoint(request: Request):
    try:
        body = (await request.body()).decode("utf-8")
        result = ingest_xml(body)
        return IngestResponse(success=True, message="XML data ingested", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ingest/csv", response_model=IngestResponse)
async def ingest_csv_endpoint(request: Request):
    try:
        body = (await request.body()).decode("utf-8")
        result = ingest_csv(body)
        return IngestResponse(success=True, message="CSV data ingested", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
