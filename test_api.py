"""Simple test API to verify FinanceAI installation and basic functionality."""

from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Import our entities to test
from finance_ai.entities.market_data import MarketData, MarketDataPoint, TimeFrame


# Response models
class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    timestamp: datetime
    service: str
    version: str


class MarketDataResponse(BaseModel):
    """Sample market data response."""
    
    symbol: str
    timeframe: str
    data_points: int
    latest_price: float
    timestamp: datetime


# Create FastAPI app
app = FastAPI(
    title="FinanceAI Test API",
    description="Simple test endpoints to verify FinanceAI installation",
    version="1.0.0",
)


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to FinanceAI Test API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        service="FinanceAI",
        version="1.0.0",
    )


@app.get("/test/market-data", response_model=MarketDataResponse)
async def test_market_data():
    """Test endpoint with sample market data using real entities."""
    
    # Create sample market data using our domain entities
    data_points = [
        MarketDataPoint(
            timestamp=datetime.now(timezone.utc),
            open_price=50000.0,
            high_price=51000.0,
            low_price=49500.0,
            close_price=50500.0,
            volume=1000.0,
        ),
        MarketDataPoint(
            timestamp=datetime.now(timezone.utc),
            open_price=50500.0,
            high_price=51500.0,
            low_price=50000.0,
            close_price=51000.0,
            volume=1200.0,
        ),
        MarketDataPoint(
            timestamp=datetime.now(timezone.utc),
            open_price=51000.0,
            high_price=52000.0,
            low_price=50800.0,
            close_price=51800.0,
            volume=1500.0,
        ),
    ]
    
    market_data = MarketData(
        symbol="BTC/USD",
        timeframe=TimeFrame.HOUR_1,
        data_points=data_points,
    )
    
    return MarketDataResponse(
        symbol=market_data.symbol,
        timeframe=market_data.timeframe.value,
        data_points=len(market_data.data_points),
        latest_price=market_data.data_points[-1].close_price,
        timestamp=datetime.now(timezone.utc),
    )


@app.get("/test/entities", response_model=Dict[str, str])
async def test_entities():
    """Test that all entities can be imported."""
    try:
        from finance_ai.entities import (
            MarketData,
            Portfolio,
            RiskAssessment,
            TradingSignal,
        )
        
        return {
            "status": "success",
            "message": "All entities imported successfully",
            "entities": "MarketData, Portfolio, RiskAssessment, TradingSignal",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to import entities: {str(e)}",
        }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting FinanceAI Test Server...")
    print("📖 API Documentation: http://127.0.0.1:8000/docs")
    print("❤️  Health Check: http://127.0.0.1:8000/health")
    print("📊 Market Data Test: http://127.0.0.1:8000/test/market-data")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
