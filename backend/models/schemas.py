from pydantic import BaseModel
from typing import Any, Optional, List


class IngestResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class PaginationInfo(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class AnalyticsData(BaseModel):
    total_orders: int
    total_revenue: float
    delayed_orders: int
    categories: List[dict]
    delivery_performance: List[dict]
    revenue_trend: List[dict]
    orders: List[dict]
    pagination: PaginationInfo


class AnalyticsResponse(BaseModel):
    success: bool
    data: AnalyticsData
