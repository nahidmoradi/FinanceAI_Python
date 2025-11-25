"""API request/response schemas for market analysis."""

from decimal import Decimal

from pydantic import BaseModel, Field


class TrendAnalysisRequest(BaseModel):
    """Request schema for trend analysis."""

    symbol: str = Field(
        description="Trading symbol to analyze",
        examples=["BTC/USD"],
        min_length=1,
    )
    timeframe: str = Field(
        description="Analysis timeframe",
        examples=["1h", "4h", "1d"],
        min_length=1,
    )
    historical_data_points: int = Field(
        default=100,
        description="Number of historical data points",
        examples=[100],
        gt=0,
        le=1000,
    )
    include_sentiment: bool = Field(
        default=True,
        description="Include sentiment analysis",
        examples=[True],
    )


class TrendAnalysisResponse(BaseModel):
    """Response schema for trend analysis."""

    symbol: str = Field(
        description="Analyzed symbol",
        examples=["BTC/USD"],
    )
    status: str = Field(
        description="Analysis status",
        examples=["completed"],
    )
    message: str = Field(
        description="Status message",
        examples=["Trend analysis completed successfully"],
    )
