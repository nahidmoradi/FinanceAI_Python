"""Market trend analysis AI agent models."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class MarketTrendAnalysisInput(BaseModel):
    """Input for market trend analysis use case."""

    symbol: str = Field(
        description="Trading symbol to analyze",
        examples=["BTC/USD"],
        min_length=1,
    )
    timeframe: str = Field(
        description="Analysis timeframe",
        examples=["1d", "1h", "4h"],
        min_length=1,
    )
    historical_data_points: int = Field(
        description="Number of historical data points to analyze",
        examples=[100],
        gt=0,
        le=1000,
    )
    include_sentiment: bool = Field(
        default=True,
        description="Include market sentiment analysis",
        examples=[True],
    )


class TrendPrediction(BaseModel):
    """Trend prediction details."""

    direction: str = Field(
        description="Predicted trend direction",
        examples=["bullish", "bearish", "sideways"],
    )
    confidence_score: Decimal = Field(
        description="Confidence score (0-100)",
        examples=[78.5],
        ge=0,
        le=100,
    )
    expected_price_target: Decimal = Field(
        description="Expected price target",
        examples=[48500.00],
        gt=0,
    )
    time_horizon: str = Field(
        description="Time horizon for prediction",
        examples=["24h", "7d", "1M"],
    )


class MarketTrendAnalysisResult(BaseModel):
    """Output from market trend analysis."""

    symbol: str = Field(
        description="Analyzed symbol",
        examples=["BTC/USD"],
    )
    current_price: Decimal = Field(
        description="Current market price",
        examples=[45123.50],
        gt=0,
    )
    trend_prediction: TrendPrediction = Field(
        description="AI-predicted trend",
    )
    key_insights: list[str] = Field(
        description="Key insights from analysis",
        examples=[["Strong momentum", "Volume increasing", "Support at $44K"]],
        min_length=1,
    )
    technical_signals: dict[str, str] = Field(
        description="Technical indicator signals",
        examples=[{"rsi": "oversold", "macd": "bullish_crossover", "ema": "above"}],
    )
    sentiment_score: Decimal | None = Field(
        default=None,
        description="Market sentiment score (-100 to 100)",
        examples=[65.3],
        ge=-100,
        le=100,
    )
    risk_factors: list[str] = Field(
        description="Identified risk factors",
        examples=[["High volatility", "Low liquidity"]],
    )
    analyzed_at: datetime = Field(
        description="Analysis timestamp",
        examples=["2024-01-15T10:30:00Z"],
    )
