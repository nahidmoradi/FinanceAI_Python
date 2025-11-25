"""Market data entities with strict validation."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TimeFrame(str, Enum):
    """Supported time frames for market data analysis."""

    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"


class MarketDataPoint(BaseModel):
    """Single data point in market time series."""

    timestamp: datetime = Field(
        description="Timestamp of the data point",
        examples=["2024-01-15T10:30:00Z"],
    )
    open_price: Decimal = Field(
        description="Opening price at this timestamp",
        examples=[45123.50],
        gt=0,
    )
    high_price: Decimal = Field(
        description="Highest price during the period",
        examples=[45500.00],
        gt=0,
    )
    low_price: Decimal = Field(
        description="Lowest price during the period",
        examples=[44800.00],
        gt=0,
    )
    close_price: Decimal = Field(
        description="Closing price at this timestamp",
        examples=[45234.75],
        gt=0,
    )
    volume: Decimal = Field(
        description="Trading volume during the period",
        examples=[1234567.89],
        ge=0,
    )

    @field_validator("high_price")
    @classmethod
    def validate_high_price(cls, value: Decimal, info: Any) -> Decimal:
        """Validate high price is greater than or equal to low price."""
        if "low_price" in info.data and value < info.data["low_price"]:
            msg = "High price must be greater than or equal to low price"
            raise ValueError(msg)
        return value

    class Config:
        frozen = True


class MarketMetrics(BaseModel):
    """Calculated metrics for market analysis."""

    moving_average_20: Decimal = Field(
        description="20-period moving average",
        examples=[45000.00],
    )
    moving_average_50: Decimal = Field(
        description="50-period moving average",
        examples=[44500.00],
    )
    relative_strength_index: Decimal = Field(
        description="RSI indicator value (0-100)",
        examples=[65.5],
        ge=0,
        le=100,
    )
    bollinger_upper: Decimal = Field(
        description="Upper Bollinger Band",
        examples=[46000.00],
    )
    bollinger_lower: Decimal = Field(
        description="Lower Bollinger Band",
        examples=[44000.00],
    )
    volume_average: Decimal = Field(
        description="Average trading volume",
        examples=[1000000.00],
        ge=0,
    )
    volatility: Decimal = Field(
        description="Price volatility percentage",
        examples=[2.5],
        ge=0,
        le=100,
    )

    class Config:
        frozen = True


class MarketData(BaseModel):
    """Complete market data entity for a financial instrument."""

    symbol: str = Field(
        description="Trading symbol or ticker",
        examples=["BTC/USD", "AAPL", "EUR/USD"],
        min_length=1,
        max_length=20,
    )
    exchange: str = Field(
        description="Exchange where the instrument is traded",
        examples=["Binance", "NYSE", "FOREX"],
        min_length=1,
        max_length=50,
    )
    time_frame: TimeFrame = Field(
        description="Time frame of the data",
        examples=[TimeFrame.ONE_HOUR],
    )
    data_points: list[MarketDataPoint] = Field(
        description="Historical data points",
        min_length=1,
    )
    metrics: MarketMetrics | None = Field(
        default=None,
        description="Calculated technical indicators",
    )
    last_updated: datetime = Field(
        description="Last update timestamp",
        examples=["2024-01-15T10:30:00Z"],
    )

    @field_validator("data_points")
    @classmethod
    def validate_data_points_order(cls, value: list[MarketDataPoint]) -> list[MarketDataPoint]:
        """Ensure data points are chronologically ordered."""
        if len(value) > 1:
            for i in range(len(value) - 1):
                if value[i].timestamp >= value[i + 1].timestamp:
                    msg = "Data points must be in chronological order"
                    raise ValueError(msg)
        return value

    class Config:
        frozen = True
