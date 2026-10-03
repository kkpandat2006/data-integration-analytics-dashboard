from fastapi import APIRouter, Query
from typing import Optional
from services.transformer import get_analytics_summary
from services.currency_service import fetch_currency_metadata
from models.schemas import AnalyticsResponse

router = APIRouter()


@router.get("/analytics/summary", response_model=AnalyticsResponse)
async def analytics_summary(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    delivery_status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    target_currency: Optional[str] = Query(None),
):
    result = get_analytics_summary(date_from, date_to, category, delivery_status, page, page_size, target_currency)
    return AnalyticsResponse(success=True, data=result)


@router.get("/analytics/currencies")
async def get_currencies():
    currencies = await fetch_currency_metadata()
    return {"success": True, "data": currencies}
